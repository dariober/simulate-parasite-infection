import copy
import numpy
import pandas
import simulate_infection as si

class Event:
    REPRODUCE = 'REPRODUCE'
    MOSQUITO_BITE = 'MOSQUITO_BITE'
    TREATMENT = 'TREATMENT'

class Host:
    """
    """
    def __init__(self, infection):
        self.infection = infection
        self.history = [copy.deepcopy(infection)]

    def reproduce_parasites(self, times= 1):
        while times > 0:
            self.infection._reproduce()
            self.history.append(copy.deepcopy(self.infection))
            times -= 1
    
    def get_infection_history(self):
        ih = [x for x in self.history if type(x) == si.infection.Infection]
        return ih

    def apply_treatment(self):
        self.history.append(Event.TREATMENT)
        for pp in self.infection.parasite_pops:
            parasite_pop = self.infection.parasite_pops[pp]
            parasite_pop.count = numpy.random.poisson(parasite_pop.count * parasite_pop.resistance, 1)[0]
        self.history.append(copy.deepcopy(self.infection))

    def mosquito_bite(self, blood_dilution):
        """Simulate a mosquito biting and sucking parasite.
        
        blood_dilution: Dilution factor representing the concentration of parasites
        in the blood. The number of parasite the mosquito will suck up is the
        product of the total number of parasites in the host times dilution
        """
        if blood_dilution > 1:
            raise Exception('Dilution cannot be > 1. Got %s' % blood_dilution)

        self.history.append(Event.MOSQUITO_BITE)

        for pp in self.infection.parasite_pops:
            tot_cnt = self.infection.parasite_pops[pp].count
            cnt = tot_cnt * blood_dilution * self.infection.parasite_pops[pp].transmissibility 
            cnt = numpy.random.poisson(cnt, 1)[0]
            if cnt > tot_cnt:
                cnt = tot_cnt
            self.infection.parasite_pops[pp].count = cnt
        self.history.append(copy.deepcopy(self.infection))

    def to_dataframe(self):
        # Create a list of list that will go into a dataframe in one shot
        data = []
        event_type = None
        i = 0
        for event in self.history:
            if event == Event.TREATMENT or event == Event.MOSQUITO_BITE:
                event_type = event
            elif type(event) == si.infection.Infection:
                if event_type is None:
                    event_type = ''
                for pop_name in event.parasite_pops:
                    pp = event.parasite_pops[pop_name]
                    line = [i, event_type, pop_name, pp.resistance, pp.repr_rate, pp.transmissibility, pp.count]
                    data.append(line)
                i += 1
                event_type = None
            else:
                raise Exception('Unexpected event in history list')
        df = pandas.DataFrame(data, columns= ['time_point', 'event', 'pop_name', 'resistance', 'repr_rate', 'transmissibility', 'count'])   
        return(df)

    def __str__(self):
        out_str = []
        for i in range(0, len(self.history)):
            out_str.append('event %s\n%s' % (i+1, self.history[i].__str__()))

        if len(out_str) > 20:
            out_str = out_str[0:10] + ['...'] + out_str[-10:]
        
        return '\n'.join(out_str)
       
