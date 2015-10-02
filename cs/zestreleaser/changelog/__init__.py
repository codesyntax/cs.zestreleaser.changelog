from zest.releaser import pypi
from zest.releaser.utils import read_text_file
from zest.releaser.utils import write_text_file
from zest.releaser.utils import execute_command
import zest.releaser.choose
import zest.releaser.git
import zest.releaser.utils


try:
    from zest.releaser.utils import system as execute_command
except ImportError:
    from zest.releaser.utils import execute_command


def fillchangelog(context):
    default_location = None
    setup_cfg = pypi.SetupConfig()
    config = setup_cfg.config
    if config and config.has_option('zest.releaser', 'history_file'):
        default_location = config.get('zest.releaser', 'history_file')

    vcs = zest.releaser.choose.version_control()
    history_file = vcs.history_file(location=default_location)
    if history_file:

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
                history_lines, history_encoding = read_text_file(history_file)
                history_lines = history_lines.split('\n')
                for line in history_lines:
                    current_position = history_lines.index(line)
                    new_history_lines.append(line)
                    if line.lower().find('unreleased') != -1:
                        # current_position + 1 == ----------------
                        # current_position + 2 ==   blank
                        # current_position + 3 == - Nothing changed yet.
                        # current_position + 4 ==   blank
                        new_history_lines.append(history_lines[current_position + 1])
                        new_history_lines.append(history_lines[current_position + 2])
                        new_history_lines.extend(pretty_data)
                        new_history_lines.extend(history_lines[current_position + 4:])
                        break

                contents = '\n'.join(new_history_lines)
                write_text_file(history_file, contents)
                msg = 'Update changelog'
                commit_cmd = vcs.cmd_commit(msg)
                commit = execute_command(commit_cmd)
                print(commit)
    else:
        print('History file not found. Skipping.')


def prettyfy_logs(data, vcs):
    """ Return a list of strings that will be injected
        into the history file
    """
    new_data = []
    if isinstance(vcs, zest.releaser.git.Git):
        # Q: How to prettyfy git logs?
        # A: Take just the lines that start with whitespaces
        author = ''
        for line in data.split(u'\n'):
            if line and line.startswith(u'Author: '):
                author = line.replace(u'Author: ', '')
            if line and line.startswith(u' '):
                if not line.strip().lower().startswith(u'back to development'):
                    new_data.append(u'- {0} [{1}]'.format(
                        line.strip(),
                        author)
                    )
                    new_data.append(u'')
    else:
        # Not implemented yet
        new_data = data.split(u'\n')

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
