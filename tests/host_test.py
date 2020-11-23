import unittest
import simulate_infection.host as hs
import simulate_infection.parasite as parasite
import simulate_infection.infection as infx
import pandas

class TestHost(unittest.TestCase):
    
    def testCanCreateInfectedHost(self):
        r_pop = parasite.ParasitePop(count= 10)
        s_pop = parasite.ParasitePop(count= 100)
        infection = infx.Infection({'R': r_pop, 'S': s_pop}, max_size= 1000)
        self.assertEqual(2, len(infection.parasite_pops))
        self.assertEqual(10, infection.parasite_pops['R'].count)
        self.assertEqual(100, infection.parasite_pops['S'].count)
        self.assertEqual(110, infection.get_total_count())
        self.assertAlmostEqual(0.09, infection.get_percentages()['R'], places= 2)

        host = hs.Host(infection= infection)

    def testCanSetTransmissibility(self):
        r_pop = parasite.ParasitePop(count= 10000, transmissibility= 1)
        infection = infx.Infection({'R': r_pop}, max_size= 1000000)
        host = hs.Host(infection= infection)
        host.mosquito_bite(blood_dilution= 0.1)
        self.assertAlmostEqual(1000, host.infection.parasite_pops['R'].count, delta= 200)

        r_pop = parasite.ParasitePop(count= 10000, transmissibility= 0)
        infection = infx.Infection({'R': r_pop}, max_size= 1000000)
        host = hs.Host(infection= infection)
        host.mosquito_bite(blood_dilution= 0.1)
        self.assertEqual(0, host.infection.parasite_pops['R'].count)

        r_pop = parasite.ParasitePop(count= 10000, transmissibility= 0.1)
        infection = infx.Infection({'R': r_pop}, max_size= 1000000)
        host = hs.Host(infection= infection)
        host.mosquito_bite(blood_dilution= 0.1)
        self.assertAlmostEqual(100, host.infection.parasite_pops['R'].count, delta= 50)

    def testHostCanReplicateOnePopParasites(self):
        pop = parasite.ParasitePop(count= 100, repr_rate= 2.5)
        infection = infx.Infection({'pop': pop}, max_size= 100000)
        host = hs.Host(infection= infection)

        host.reproduce_parasites(times= 30)
        last_pop = host.get_infection_history()[-1]
        self.assertTrue(last_pop.parasite_pops['pop'].count > 55000 and last_pop.parasite_pops['pop'].count < 65000)

        # repr_rate < 1: Pop does not support itself
        start = 100
        pop = parasite.ParasitePop(count= start, repr_rate= 0.7)
        infection = infx.Infection({'pop': pop}, max_size= 100000)
        host = hs.Host(infection= infection)

        host.reproduce_parasites(times= 30)
        last_pop = host.get_infection_history()[-1]
        self.assertTrue(last_pop.parasite_pops['pop'].count < start)

    def testHostCanReplicateTwoEqualPops(self):
        pop1 = parasite.ParasitePop(count= 100, repr_rate= 1.5)
        pop2 = parasite.ParasitePop(count= 100, repr_rate= 1.5)
        infection = infx.Infection({'pop1': pop1, 'pop2': pop2}, max_size= 1000000)
        host = hs.Host(infection= infection)
        
        host.reproduce_parasites(times= 20)
        last_pop = host.get_infection_history()[-1]
        df = host.to_dataframe()
        x = list(df[df.pop_name == 'pop1']['count'])
        y = list(df[df.pop_name == 'pop2']['count'])
        diff = [x[i] - y[i] for i in range(len(x))]
        self.assertAlmostEqual(0, max(diff), delta= 100000)

    def testHostCanReplicateParasites(self):
        s_pop = parasite.ParasitePop(count= 100, repr_rate= 1.5)
        f_pop = parasite.ParasitePop(count= 100, repr_rate= 2)
        infection = infx.Infection({'slow': s_pop, 'fast': f_pop}, max_size= 10000000)
        host = hs.Host(infection= infection)

        host.reproduce_parasites(times= 10)
        ih = host.get_infection_history()
        self.assertEqual(11, len(ih))

        last_pop = ih[-1]
        self.assertTrue(last_pop.parasite_pops['slow'].count > 1000 and last_pop.parasite_pops['slow'].count < 8000)
        self.assertTrue(last_pop.parasite_pops['fast'].count > 60000 and last_pop.parasite_pops['fast'].count < 150000)

        self.assertEqual(last_pop.__str__(), host.infection.__str__())

    def testHostTreatement(self):
        r_pop = parasite.ParasitePop(count= 100, resistance= 1)
        s_pop = parasite.ParasitePop(count= 100, resistance= 0.01)
        infection = infx.Infection({'R': r_pop, 'S': s_pop}, max_size= 1000000)
        host = hs.Host(infection= infection)

        host.apply_treatment()
        self.assertTrue(host.infection.parasite_pops['R'].count > 10 and host.infection.parasite_pops['R'].count < 1000)
        self.assertTrue(host.infection.parasite_pops['S'].count < 10)
        
        # Treatment has been recorded in history:
        self.assertEqual('TREATMENT', host.history[-2])
        self.assertEqual(host.history[-1].parasite_pops['R'].count, host.infection.parasite_pops['R'].count)

    def testTryReproduceZeroParasites(self):
        s_pop = parasite.ParasitePop(count= 10)
        infection = infx.Infection({'S': s_pop}, max_size= 1000000)
        host = hs.Host(infection= infection)

        host.apply_treatment()
        host.apply_treatment()
        self.assertEqual(0, host.infection.parasite_pops['S'].count)
        host.reproduce_parasites(times= 10)
        self.assertEqual(0, host.infection.parasite_pops['S'].count)

    def testMosquitoBite(self):
        r_pop = parasite.ParasitePop(count= 200000)
        s_pop = parasite.ParasitePop(count= 800000)
        infection = infx.Infection({'R': r_pop, 'S': s_pop}, max_size= 10000000)
        host = hs.Host(infection= infection)

        host.mosquito_bite(blood_dilution= 1e-2)
        self.assertTrue(host.infection.parasite_pops['R'].count > 1500 and host.infection.parasite_pops['R'].count < 2500)
        self.assertTrue(host.infection.parasite_pops['S'].count > 7500 and host.infection.parasite_pops['S'].count < 8500)

        r_pop = parasite.ParasitePop(count= 20)
        s_pop = parasite.ParasitePop(count= 80)
        infection = infx.Infection({'R': r_pop, 'S': s_pop}, max_size= 10000)
        host = hs.Host(infection= infection)
        
        xpass= False
        try:
            host.mosquito_bite(blood_dilution= 1.1)
        except:
            xpass = True
        self.assertTrue(xpass)

        host.mosquito_bite(blood_dilution= 1e-9)
        self.assertEqual(0, host.infection.get_total_count())

        self.assertEqual('MOSQUITO_BITE', host.history[-2])
        self.assertEqual(host.history[-1].parasite_pops['R'].count, host.infection.parasite_pops['R'].count)

    def testHistoryToDataFrame(self):
        r_pop = parasite.ParasitePop(count= 200000, resistance= 0.9)
        s_pop = parasite.ParasitePop(count= 800000, resistance= 0.2)
        infection = infx.Infection({'R': r_pop, 'S': s_pop}, max_size= 10000000)
        host = hs.Host(infection= infection)

        host.mosquito_bite(blood_dilution= 1e-4)
        host.reproduce_parasites(times= 8)
        host.apply_treatment()
        df = host.to_dataframe()

        self.assertEqual(['count', 'event', 'pop_name', 'repr_rate', 'resistance', 'time_point', 'transmissibility'], sorted(df.columns))
        self.assertEqual(22, df.shape[0])
        self.assertEqual(['R', 'S'] * int(df.shape[0]/2), list(df['pop_name']))
        self.assertEqual([0.9, 0.2] * int(df.shape[0]/2), list(df['resistance']))
        self.assertEqual([200000, 800000], list(df['count'][0:2]))
        self.assertTrue(df['count'][2] < 1000)
        self.assertTrue(df['count'][20] > 1000)
        self.assertEqual('MOSQUITO_BITE', df['event'][2])
        self.assertEqual('TREATMENT', df['event'][20])

        tp = [x for x in range(0, 11) for i in range(2)]
        self.assertEqual(tp, list(df['time_point']))

if __name__ == '__main__':
    unittest.main()
