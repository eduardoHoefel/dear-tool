from functools import reduce
import numpy as np

class Statistics():

    def __init__(self, it, f):
        self.run(it, f)

    def build_stats(d):
        keys = d.keys()

        stats = {}
        for i in keys:
            data = d[i]

            k_stats = {}

            k_stats['min'] = min(data)
            k_stats['max'] = max(data)
            k_stats['avg'] = np.mean(data)
            k_stats['std'] = np.std(data)

            stats[i] = k_stats

        return stats

    def sort_stats(d):
        keys = d.keys()

        sorted_stats = {}

        sorted_stats['min'] = sorted(keys, key=lambda x: d[x]['min'])
        sorted_stats['max'] = sorted(keys, key=lambda x: d[x]['max'])
        sorted_stats['avg'] = sorted(keys, key=lambda x: d[x]['avg'])
        sorted_stats['std'] = sorted(keys, key=lambda x: d[x]['std'])

        return sorted_stats

    def run(self, it, f):

        g_data = {}
        g_pos = {}

        for i in range(it):
            r_i = f()
            cycle_data = {}
            for j in r_i.keys():
                r_j = r_i[j]
                if j not in g_data:
                    g_data[j] = []
                    g_pos[j] = []

                g_data[j].append(r_j)
                cycle_data[j] = r_j

            keys = r_i.keys()
            cycle_sorted = sorted(keys, key=lambda x: cycle_data[x])
            for j in range(len(keys)):
                key = cycle_sorted[j]
                g_pos[key].append(j)

        g_data_stats = Statistics.build_stats(g_data)
        g_data_sorted_stats = Statistics.sort_stats(g_data_stats)

        g_pos_stats = Statistics.build_stats(g_pos)
        g_pos_sorted_stats = Statistics.sort_stats(g_pos_stats)

        self.stats = {}
        self.stats['data'] = g_data_stats
        self.stats['data_stats'] = g_data_sorted_stats
        self.stats['pos'] = g_pos_stats
        self.stats['pos_stats'] = g_pos_sorted_stats

    def build_stats_string(keys_presented, name, data, data_stats, index):
        build_str = "    {}:\n".format(name)
        for key in data_stats.keys():
            best_key = data_stats[key][index]
            best_value = data[best_key][key]
            build_str += "      {}: \t\t{}\t{}\n".format(key, best_key, best_value)

            if best_key not in keys_presented:
                keys_presented[best_key] = []

            keys_presented[best_key].append("{}[{}]".format(name, key))
        
        return build_str

    def __str__(self):
        keys_presented = {}

        build_str = "Statistics:\n"
        build_str += "  Total participants:\t{}\n".format(len(self.stats['data']))

        build_str += "\n  Top:\n"
        build_str += Statistics.build_stats_string(keys_presented, "Data (lowest)", self.stats['data'], self.stats['data_stats'], 0)
        build_str += Statistics.build_stats_string(keys_presented, "Pos (lowest)", self.stats['pos'], self.stats['pos_stats'], 0)
        build_str += Statistics.build_stats_string(keys_presented, "Data (highest)", self.stats['data'], self.stats['data_stats'], -1)
        build_str += Statistics.build_stats_string(keys_presented, "Pos (highest)", self.stats['pos'], self.stats['pos_stats'], -1)


        build_str += "\n  Winners:\n"
        for k in keys_presented.keys():
            build_str += "    {}:\n".format(k)
            for trophy in keys_presented[k]:
                build_str += "      \t{}\n".format(trophy)

            key_data_stats = self.stats['data'][k]

            build_str += "      Data stats:\n"
            for stat in key_data_stats.keys():
                build_str += "        {}:\t{}\n".format(stat, key_data_stats[stat])

            key_pos_stats = self.stats['pos'][k]

            build_str += "      Pos stats:\n"
            for stat in key_pos_stats.keys():
                build_str += "        {}:\t{}\n".format(stat, key_pos_stats[stat])

            build_str += "\n"



        return build_str
