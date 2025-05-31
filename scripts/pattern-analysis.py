import pandas as pd
import ast

def print_msg_box(msg, indent=1, width=None, title=None):
    # credit to https://stackoverflow.com/a/58780542
    """Print message-box with optional title."""
    lines = msg.split('\n')
    space = " " * indent
    if not width:
        width = max(map(len, lines))
    box = f'╔{"═" * (width + indent * 2)}╗\n'  # upper_border
    if title:
        box += f'║{space}{title:<{width}}{space}║\n'  # title
        box += f'║{space}{"-" * len(title):<{width}}{space}║\n'  # underscore
    box += ''.join([f'║{space}{line:<{width}}{space}║\n' for line in lines])
    box += f'╚{"═" * (width + indent * 2)}╝'  # lower_border
    print(box)


def get_link_to_report(bug_id):
    return 'https://issues.apache.org/jira/browse/' + bug_id


def read_bug_reports(csv_file_path):
    return pd.read_csv(csv_file_path, converters={'Tags': ast.literal_eval})


def find_all_bugs_with_tag(df, tag):
    return df[df['Tags'].apply(lambda x: tag in x)]

def get_bug_ids_with_tag(df, tag):
    return df[df['Tags'].apply(lambda x: tag in x)]['ID'].tolist()

def bug_has_tag(df, bug_id, tag):
    return tag in df[df['ID'] == bug_id]['Tags'].tolist()[0]

def bug_has_tag_in_list(df, bug_id, tags):
    return any([tag in df[df['ID'] == bug_id]['Tags'].tolist()[0] for tag in tags])

def get_bug_ids_has_tag_prefix(df, tag_prefix):
    return df[df['Tags'].apply(lambda x: any([tag.startswith(tag_prefix) for tag in x]))]['ID'].tolist()


if __name__ == '__main__':
    df_all_bug_reports = read_bug_reports('pattern-study/scalability-bugs.csv')

    print('Total number of bugs: {}'.format(len(df_all_bug_reports)))

    # get a list of all tags exist
    all_tags = set()
    for tags in df_all_bug_reports['Tags']:
        all_tags.update(tags)
    all_tags = list(all_tags)

    # get percentage breakdown for each root causes
    print_msg_box('Pattern compute Breakdown', title='Section 2')
    rc_compute_tags = [tag for tag in all_tags if tag.startswith('rc-compute')]
    rc_compute_types = {
        'total': rc_compute_tags,
        'compute-cross': ['rc-compute-cross'],
        'compute-sync': ['rc-compute-sync'],
        'compute-app': ['rc-compute-app']
    }

    rc_compute_bugs = sum([get_bug_ids_with_tag(df_all_bug_reports, tag) for tag in rc_compute_tags], [])
    print('In total of {} bugs, {} ({}%) are rc-compute'.format(len(df_all_bug_reports), len(rc_compute_bugs), round(len(rc_compute_bugs) / len(df_all_bug_reports) * 100, 2)))
    # get breakdown of sub-types
    for compute_type in rc_compute_types.keys():
        sub_type_bugs = [get_bug_ids_with_tag(df_all_bug_reports, tag) for tag in rc_compute_types[compute_type]]
        sub_type_bugs = [bug for bugs in sub_type_bugs for bug in bugs]
        sub_type_bugs = list(set(sub_type_bugs))
        print('{}: {} bugs -> {}%.'.format(compute_type, len(sub_type_bugs), round(len(sub_type_bugs) / len(rc_compute_bugs) * 100, 2)))

    #############################################################################
    print_msg_box('Pattern unbound Breakdown', title='Section 2')
    rc_unbound_tags = [tag for tag in all_tags if tag.startswith('rc-unbound')]
    rc_unbound_types = {
        'tt': rc_unbound_tags,
        'unbound-persistent': ['rc-unbound-persistent'],
        'unbound-temporary': ['rc-unbound-temporary'],
        'unbound-os': ['rc-unbound-os'],
    }

    rc_unbound_bugs = sum([get_bug_ids_with_tag(df_all_bug_reports, tag) for tag in rc_unbound_tags], [])
    print('In total of {} bugs, {} ({}%) are rc-unbound'.format(len(df_all_bug_reports), len(rc_unbound_bugs), round(len(rc_unbound_bugs) / len(df_all_bug_reports) * 100, 2)))
    # get breakdown of sub-types
    for unbound_type in rc_unbound_types.keys():
        sub_type_bugs = [get_bug_ids_with_tag(df_all_bug_reports, tag) for tag in rc_unbound_types[unbound_type]]
        sub_type_bugs = [bug for bugs in sub_type_bugs for bug in bugs]
        sub_type_bugs = list(set(sub_type_bugs))
        print('{}: {} bugs -> {}%.'.format(unbound_type, len(sub_type_bugs), round(len(sub_type_bugs) / len(rc_unbound_bugs) * 100, 2)))


    #############################################################################
    print_msg_box('Pattern bloat Breakdown', title='Section 2')
    rc_bloat_tags = [tag for tag in all_tags if tag.startswith('rc-bloat')]
    rc_bloat_types = {
        'total': rc_bloat_tags,
        'bloat-waste': ['rc-bloat-waste'],
        'bloat-opt': ['rc-bloat-opt']
    }

    rc_bloat_bugs = sum([get_bug_ids_with_tag(df_all_bug_reports, tag) for tag in rc_bloat_tags], [])
    print('In total of {} bugs, {} ({}%) are rc-bloat'.format(len(df_all_bug_reports), len(rc_bloat_bugs), round(len(rc_bloat_bugs) / len(df_all_bug_reports) * 100, 2)))
    # get breakdown of sub-types
    for bloat_type in rc_bloat_types.keys():
        sub_type_bugs = [get_bug_ids_with_tag(df_all_bug_reports, tag) for tag in rc_bloat_types[bloat_type]]
        sub_type_bugs = [bug for bugs in sub_type_bugs for bug in bugs]
        sub_type_bugs = list(set(sub_type_bugs))
        print('{}: {} bugs -> {}%.'.format(bloat_type, len(sub_type_bugs), round(len(sub_type_bugs) / len(rc_bloat_bugs) * 100, 2)))

    #############################################################################
    print_msg_box('Pattern logic Breakdown', title='Section 2')
    rc_logic_tags = [tag for tag in all_tags if tag.startswith('rc-logic')]
    rc_logic_types = {
        'total': rc_logic_tags,
        'logic-leak': ['rc-logic-leak'],
        'logic-race': ['rc-logic-race'],
        'logic-corner': ['rc-logic-corner']
    }

    rc_logic_bugs = sum([get_bug_ids_with_tag(df_all_bug_reports, tag) for tag in rc_logic_tags], [])
    print('In total of {} bugs, {} ({}%) are rc-logic'.format(len(df_all_bug_reports), len(rc_logic_bugs), round(len(rc_logic_bugs) / len(df_all_bug_reports) * 100, 2)))
    # get breakdown of sub-types
    for logic_type in rc_logic_types.keys():
        sub_type_bugs = [get_bug_ids_with_tag(df_all_bug_reports, tag) for tag in rc_logic_types[logic_type]]
        sub_type_bugs = [bug for bugs in sub_type_bugs for bug in bugs]
        sub_type_bugs = list(set(sub_type_bugs))
        print('{}: {} bugs -> {}%.'.format(logic_type, len(sub_type_bugs), round(len(sub_type_bugs) / len(rc_logic_bugs) * 100, 2)))
    

    



