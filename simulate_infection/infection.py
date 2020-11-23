import numpy
import simulate_infection.parasite as parasite
import math
import random

class Infection:
    def __init__(self, parasite_pops, max_size):
        """parasite_pops: Dictionary of ParasitePop with key being the name of the population
        max_size: The maximum number of parasites that the infection can sustain.
        """
        if type(parasite_pops) != dict:
            raise Exception('parasite_pops must be a dictionary of ParasitePop objects')
        for pp in parasite_pops:
            if type(parasite_pops[pp]) != parasite.ParasitePop:
                raise Exception('Not all entries in parasite_pops are ParasitePop objects')
        if max_size <= 0:
            raise Exception('max_size must be > 0')   

        self.parasite_pops = parasite_pops
        self.max_size = max_size
        
        if self.get_total_count() > self.max_size:
            raise Exception('Total size of input parasite populations exceeds the max_size of this infection')

    def get_total_count(self):
        N = 0
        for pp in self.parasite_pops:
            N += self.parasite_pops[pp].count
        return N

    def get_percentages(self):
        N = self.get_total_count()
        pct = {}
        for pp in self.parasite_pops.keys():
            pct[pp] = self.parasite_pops[pp].count / N
        return pct

    def _reproduce(self):
        start_counts = {}
        end_counts = {}
        for pp in self.parasite_pops:
            start_counts[pp] = self.parasite_pops[pp].count
            end_counts[pp] = 0

        # We replicate the different populations in small bursts of size
        # chunk_size to approximate concurrent growth. If we reproduce a
        # population all in one call, the first pop to reproduce would be
        # favoured
        chunk_size = math.ceil(max(start_counts.values()) / 200)
        while sum(start_counts.values()) > 0:
            # We randomize which pop to reproduce first so we don't give any
            # sytematic advantage to any
            pops = list(self.parasite_pops.keys())
            random.shuffle(pops)
            for pp in pops:
                if start_counts[pp] <= 0:
                    continue
                count = min([chunk_size, start_counts[pp]])
                start_counts[pp] -= count
                chunk_pct = count / self.parasite_pops[pp].count
                free_space = (self.parasite_pops[pp].count + (self.max_size - self.get_total_count())) * chunk_pct
                pct_max = count / free_space 
                if pct_max >= 1:
                    pct_max = 1/self.max_size
                pp_growth_pct = self._logitic_map(self.parasite_pops[pp].repr_rate, pct_max)
                end_counts[pp] += free_space * pp_growth_pct

        for pp in self.parasite_pops:
            self.parasite_pops[pp].count = numpy.random.poisson(end_counts[pp], 1)[0]
    
        #for pp in self.parasite_pops:
        #    # Max size that this population can grow. It's the current size of
        #    # this population + what is not occupied by the other pops in the
        #    # infection
        #    pp_max_size = self.parasite_pops[pp].count + (self.max_size - self.get_total_count())
        #    pct_max = self.parasite_pops[pp].count / pp_max_size 
        #    if pct_max >= 1:
        #        pct_max = 1/self.max_size
        #    pp_growth_pct = self._logitic_map(self.parasite_pops[pp].repr_rate, pct_max)
        #    pp_new_count = pp_max_size * pp_growth_pct
        #    self.parasite_pops[pp].count = numpy.random.poisson(pp_new_count, 1)[0]

    def _logitic_map(self, repr_rate, pct_max):
        x_next = repr_rate * pct_max * (1 - pct_max)
        return x_next 

    def __str__(self):
        out_str = []
        for pp in sorted(self.parasite_pops.keys()):
            out_str.append('%s: %s' % (pp, self.parasite_pops[pp]))
        return '\n'.join(out_str)
