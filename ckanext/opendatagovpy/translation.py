__author__ = 'Rodrigo Parra'

import pylons.config as config
from logging import getLogger
from subprocess import Popen, PIPE
import os

import ckan.plugins.toolkit as toolkit


log = getLogger(__name__)


class TranslationsCommand(toolkit.CkanCommand):
    '''
    Merges CKAN base .po file with .po files defined by extensions.
    Output is generated in the directory specified by ckan.i18n_directory config setting.

    Usage::

        paster translations merge -c <path to config file>

    The commands should be run from the ckanext-opendatagovpy directory.
    '''
    summary = __doc__.split('\n')[0]
    usage = __doc__

    CKAN_PO_FILE = '../ckan/ckan/i18n/{0}/LC_MESSAGES/ckan.po'
    CKAN_MO_FILE = '{0}/i18n/{1}/LC_MESSAGES/ckan.mo'
    EXT_FILE = '../{0}/ckanext/{1}/i18n/{2}/LC_MESSAGES/{3}.po'

    def __init__(self, name):
        super(TranslationsCommand, self).__init__(name)
        self.parser.add_option('-l', '--lang', dest='lang',
            default='es', help='Language code of the .po files to merge.')


    def command(self):
        '''
        Parse command line arguments and call appropriate method.
        '''
        if not self.args or self.args[0] in ['--help', '-h', 'help']:
            print TranslationsCommand.__doc__
            return

        cmd = self.args[0]
        self._load_config()

        if cmd == 'merge':
            self._merge_files()
        else:
            log.error('Command "%s" not recognized' % (cmd,))


    def _merge_files(self):
        parent_dir = os.path.join(os.getcwd(), os.pardir)
        extension_dirs = [name for name in os.listdir(parent_dir) if os.path.isdir(os.path.join(parent_dir, name))
                            and name.startswith('ckanext-')]

        files = [self.CKAN_PO_FILE.format(self.options.lang)]
        for dir in extension_dirs:
            file = self._get_file_path(dir)
            if file:
                files.append(file)

        dest_dir = config.get('ckan.i18n_directory')
        if dest_dir:
            output = self.CKAN_MO_FILE.format(dest_dir, self.options.lang)
            print output
            msgcat = Popen(['msgcat', '--use-first'] +  files, stdout=PIPE)
            msgfmt = Popen(['msgfmt', '-', '-o', output], stdin=msgcat.stdout, stdout=PIPE)
        else:
            log.error('Config property "ckan.i18n_directory" not set.')


    def _get_file_path(self, dir):
        ext_name =dir.replace('ckanext-', '')
        path = self.EXT_FILE.format(dir, ext_name, self.options.lang, dir)
        if os.path.isfile(path):
            return path
        else:
            return ''