import zest.releaser.choose
import zest.releaser.utils
import zest.releaser.git

from copy import copy


try:
    from zest.releaser.utils import system as execute_command
except ImportError:
    from zest.releaser.utils import execute_command


def fillchangelog(context):
    vcs = zest.releaser.choose.version_control()
    try:
        found = zest.releaser.utils.get_last_tag(vcs)
        log_command = vcs.cmd_log_since_tag(found)
    except SystemExit:
        log_command = get_all_commits_command(vcs)

    if log_command:
        data = execute_command(log_command)
        pretty_data = prettyfy_logs(data, vcs)

        print('These are all the commits since the last tag:')
        print('')
        print('\n'.join(pretty_data))

        if zest.releaser.utils.ask('Do you want to add those commits to the CHANGES file?', True):
            new_history_lines = []
            history_lines = copy(context.get('history_lines', []))
            for line in history_lines:
                current_position = history_lines.index(line)
                new_history_lines.append(line)
                if line.startswith('%s ' % context.get('new_version')):
                    # current_position + 1 == ----------------
                    # current_position + 2 ==   blank
                    # current_position + 3 == - Nothing changed yet.
                    # current_position + 4 ==   blank
                    new_history_lines.append(history_lines[current_position + 1])
                    new_history_lines.append(history_lines[current_position + 2])
                    new_history_lines.extend(pretty_data)
                    new_history_lines.extend(history_lines[current_position + 4:])
                    break

            context.update({'history_lines': new_history_lines})


def prettyfy_logs(data, vcs):
    """ Return a list of strings that will be injected
        into the history file
    """
    new_data = []
    if isinstance(vcs, zest.releaser.git.Git):
        # Q: How to prettyfy git logs?
        # A: Take just the lines that start with whitespaces
        author = ''
        for line in data.split('\n'):
            if line and line.startswith('Author: '):
                author = line.replace('Author: ', '')
            if line and line.startswith(' '):
                if not line.strip().lower().startswith('back to development'):
                    new_data.append('- {0} [{1}]'.format(
                        line.strip(),
                        author)
                    )
                    new_data.append('')
    else:
        # Not implemented yet
        new_data = data.split('\n')

    return new_data


def get_all_commits_command(vcs):
    if isinstance(vcs, zest.releaser.git.Git):
        return 'git log'
    elif isinstance(vcs, zest.releaser.bzr.Bzr):
        return 'bzr log'
    elif isinstance(vcs, zest.releaser.hg.Hg):
        return 'hg log'
    elif isinstance(vcs, zest.releaser.svn.Svn):
        url = vcs._svn_info()
        return 'svn --non-interactive log %s' % url
