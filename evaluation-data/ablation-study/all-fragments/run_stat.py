import os,sys
import pandas as pd
import numpy as np


def get_dimensional_methods(system_tag):
    system_tag_lower = system_tag.replace('.', '_').replace('-', '_')
    qll_file = f'dimensional_{system_tag_lower}.qll'
    qll_path = os.path.join(os.getcwd(), 'queries', qll_file)
    with open(qll_path, 'r') as f:
        lines = f.readlines()
    dcfs = []
    for line in lines:
        line = line.strip()
        if line.startswith('\"'):
            line = line.replace(',', '')
            line = line.replace('\"', '')
            dcfs.append(line)
    return dcfs

def get_dimensional_loops(system_tag):
    csv_file = os.path.join(os.getcwd(), f'{system_tag}.csv')
    df = pd.read_csv(csv_file, header=None, names=['DCF', 'Line', 'Type'])
    return df['DCF'].values.tolist()

def _codeql_parser(ql_results):
    ql_results = ql_results.splitlines()
    ql_results = ql_results[2:]
    methods = []
    for line in ql_results:
        line = line.strip()
        if line.startswith('|'):
            method = line.split('|')[1].strip()
            methods.append(method)
    return methods

def get_pattern_dimensional(system_tag, pattern):
    query_output = f'{system_tag}-{pattern}.txt'
    with open(query_output, 'r') as f:
        ql_stdout = f.read()
    dcf_list = _codeql_parser(ql_stdout)
    return dcf_list

def main():
    system_tags = ['CA-4.1.0', 'HD-3.4.0', 'IG-2.16.0']
    patterns = ['compute-sync', 'compute-app', 'compute-cross', 'unbound-collection', 'unbound-allocation', 'unbound-os']

    for system_tag in system_tags:
        methods = get_dimensional_methods(system_tag)
        loops = get_dimensional_loops(system_tag)

        dcfs = methods + loops

        print(f'DCFs in {system_tag}: {len(dcfs)}')
        pattern_dcfs = {}
        for pattern in patterns:
            dcf_list = get_pattern_dimensional(system_tag, pattern)
            pattern_dcfs[pattern] = dcf_list
            print(f'{pattern}: {len(dcf_list)}')
        all_pattern_dcfs = sum(pattern_dcfs.values(), [])
        print(f'Totally: {len(all_pattern_dcfs)}')
        unique_dcfs = set(all_pattern_dcfs)
        print(f'Deduplicated: {len(unique_dcfs)}')

        MAKE_CSV = True
        if MAKE_CSV:
            num_patterns_stat = {}
            df = pd.DataFrame(columns=['DCF', 'Flagged'] + patterns)
            for dcf in unique_dcfs:
                row = {'DCF': dcf, 'Flagged': dcf in unique_dcfs}
                for pattern in patterns:
                    row[pattern] = dcf in pattern_dcfs[pattern]

                num_patterns = sum(row[pattern] for pattern in patterns)
                if num_patterns not in num_patterns_stat:
                    num_patterns_stat[num_patterns] = 0
                num_patterns_stat[num_patterns] += 1
                df.loc[len(df)] = row
            df.to_csv(f'{system_tag}-patterns.csv', index=False)
            print(f'Pattern statistics: {num_patterns_stat}')
if __name__ == '__main__':
    main()

