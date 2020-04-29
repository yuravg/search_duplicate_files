"""
Search Duplicate files
"""

import os
from os import stat
from os.path import expanduser
import sys
from datetime import datetime
from .yes_no import yes_no
from .files import movefile
from .makedir import makedir
from .progressbar import ProgressBar
from .md5sum import md5hex
from .removetree import removetree


class SearchDuplicateFiles(object):
    """Search Duplicate files
    """
    def __init__(self, args):
        if args.path == []:
            path = ['.']
        else:
            path = args.path
        for __p in path:
            if not os.path.exists(__p):
                sys.exit("ERROR! Don't exists selected path: %s\nExit from program!" % __p)
        self.flist = []
        cur_dir = os.getcwd()
        self.arguments_msg = " Search duplicate files:\
        \n  current directory = '%s'\
        \n  search  directory = '%s'\
        \n  mask        = '%s'\
        \n  size        = '%s'\
        \n  name        = '%s'\
        \n  md5sum      = '%s'\
        \n  move        = '%s'\
        \n  ignore mask = '%s'\
        \n  delete      = '%s'\
        \n  interactive = '%s'\
        \n  warning     = '%s'\
        \n  write_log   = '%s'\
        \n  verbose     = '%s'\n" % (cur_dir, path, args.mask, args.size_en, args.name_en,
                                     args.sum_en, args.move_en, args.ignore_mask, args.delete_en,
                                     args.interactive, args.warning, args.write_log, args.verbose)
        if args.mask != '':
            self.mask = args.mask.split()
        else:
            self.mask = ['']
        self.run(self.mask, path, args)

    def flist_add(self, i):
        self.flist.append(i)

    def flist_del(self):
        self.flist = []

    def run(self, mask, path, args):
        if args.show_arguments:
            print(self.arguments_msg)
        move_allowed = False
        delete_allowed = False
        if args.move_en:
            if args.warning:
                if yes_no('Would you like move duplicate files', True):
                    move_allowed = True
                else:
                    print('\nNOTE:\nSearch duplicate without move files!')
            else:
                move_allowed = True
        else:
            if args.delete_en:
                if args.warning:
                    print('\n')
                    print('+--------------------------------------------------------------+')
                    print("|  NOTE: you are going to REMOVE duplicate files,              |")
                    print("|   better way use 'move' to temporary directory, see at help  |")
                    print('+--------------------------------------------------------------+')
                    print('\n')
                    if yes_no('Would you like DELETE duplicate files', True):
                        delete_allowed = True
                    else:
                        print('\nNOTE:\nSearch duplicate without move files!')
                else:
                    delete_allowed = True
        self.search(mask, path, args)
        if args.verbose:
            if self.length_flist():
                print('')
                print('+------------------------------+')
                print('| Duplicate log:               |')
                print('+------------------------------+')
                print('%s' % self.__str__())
        print(self.str_summary())
        if args.write_log:
            self.write_log_file(self.full_info())
        if move_allowed or delete_allowed:
            self.move_or_delete(args)

    def search(self, mask, path, args):
        pb = Progress()
        pb.show(False)
        files_in_dir = 0
        for __p in path:
            files_in_dir = files_in_dir + self.calc_files_in_directory(__p)
        pb.set_steps(files_in_dir * 2)
        pb.msg_files(files_in_dir)
        lst0 = []
        for __p in path:
            lst0.extend(self.get_list_by_mask(mask, __p, args.ignore_mask, pb))
        lst1 = lst0[:]
        files_in_mask = len(lst0)
        pb.msg_files_in_files(files_in_mask, files_in_dir)
        files_un_mask = files_in_dir - files_in_mask
        pb.repeat_show(files_un_mask)
        if args.name_en:
            self.search_duplicate_by_name(lst0, lst1, pb)
        else:
            self.flist_add(lst0)
            pb.repeat_show(files_in_mask)
        if args.size_en:
            self.search_by_size(self.flist)
        if args.sum_en:
            if not args.size_en:
                self.search_by_size(self.flist)
            self.search_by_md5sum(self.flist)

    def get_list_by_mask(self, mask, path, ignore_mask, pb):
        l = []
        for root, dirs, files in os.walk(path):
            for f in files:
                pb.show()
                fpath = os.path.join(root, f)
                if self.not_in_ignore_mask(fpath, ignore_mask):
                    if mask == []:
                        l.append(fpath)
                    elif any(f.endswith(ext) for ext in mask):
                        l.append(fpath)
        l_sorted = sorted(l)
        return l_sorted

    def not_in_ignore_mask(self, name, ignore_mask):
        name = name.replace("\\", "/")
        is_in_mask = False
        for mask in ignore_mask:
            if name.find(mask) != -1:
                is_in_mask = True
                break
        return not is_in_mask

    def search_duplicate_by_name(self, lst0, lst1, pb):
        for i in lst0:
            self.search_in_list(i, lst1)
            pb.show()

    def search_in_list(self, path, lst):
        res_lst = []
        name = os.path.basename(path)
        if len(lst) > 0:
            in_lst = lst[:]
            index = 0
            for i in in_lst:
                i_name = os.path.basename(i)
                if name == i_name:
                    res_lst.append(i)
                    del lst[index]
                else:
                    index += 1
            if len(res_lst) > 1:
                self.flist.append(res_lst)

    def length_flist(self):
        return len(self.flist)

    @staticmethod
    def duplicate_file_path(lst):
        return lst[1:]

    def str_summary(self):
        return 'Summary: find %s duplicate file(s)' % self.length_flist()

    def __str__(self):
        s = ''
        for i in range(self.length_flist()):
            flist = self.flist[i]
            fname = os.path.basename(flist[0])
            s = '%s\nfile: %s\n' % (s, fname)
            first = True
            for fi in flist:
                if first:
                    msg = ' (first from: %s)' % len(flist)
                else:
                    msg = ''
                s = '%s%s%s\n' % (s, fi, msg)
                first = False
        return s

    def full_info(self):
        s = '%s\n' % self.arguments_msg + self.__str__()
        return s

    @staticmethod
    def write2file(data, fname, verbose=True):
        """write data to file"""
        f = open(fname, 'w', newline='\n')
        f.write(data)
        f.close()
        if verbose:
            print('Write file: %s' % fname)

    def write_log_file(self, data):
        date = self.date2string()
        home = expanduser("~")
        fname = '%s/tmp/Duplicate-%s.log' % (home, date)
        data = (date + '\n' + '-'*19 + '\n'*2 + data)
        self.write2file(data, fname)

    def move_or_delete(self, args):
        path2move = ''
        if args.move_en:
            if path2move == '':
                date = self.date2string()
                path2move = 'zz!zzDUPLICATES-%s' % date
                makedir(path2move)
        for i in range(self.length_flist()):
            flist = self.flist[i]
            fname = os.path.basename(flist[0])
            print("\nDuplicate file: '%s' and list:" % fname)
            for fi in flist:
                index = flist.index(fi)
                print('%s. %s' % (index, fi))
            for fi in flist:
                index = flist.index(fi)
                out_fname = "%s/%s" % (path2move, os.path.basename(fi))
                if args.interactive:
                    finf = '%s. %s' % (index, fi)
                    if yes_no("Would you like delete file: '%s'" % finf):
                        self.move_or_delete_file(args, fi, out_fname)
                else:
                    if index:
                        self.move_or_delete_file(args, fi, out_fname)
        if args.delete_en and args.move_en:
            question = "\nWould you like delete directory with duplicate files: %s" % path2move
            if yes_no(question, True):
                removetree(path2move)

    @staticmethod
    def move_or_delete_file(args, fname, out_fname):
        if args.move_en:
            movefile(fname, out_fname, False, True, True)
        else:
            os.remove(fname)

    def search_by_size(self, dup_lst):
        self.flist_del()
        lst = self.calc_size(dup_lst)
        self.search_in_list_of_list(lst)

    def search_by_md5sum(self, dup_lst):
        self.flist_del()
        lst = self.calc_sum(dup_lst)
        self.search_in_list_of_list(lst)

    @staticmethod
    def calc_size(dup_lst):
        dup_lst = dup_lst[:]
        lst_f_size = []
        for i in dup_lst:
            f_size = []
            for path in i:
                size = stat(path).st_size
                f_size.append(size)
                f_size.append(path)
            lst_f_size.append(f_size)
        return lst_f_size

    @staticmethod
    def calc_sum(dup_lst):
        dup_lst = dup_lst[:]
        lst_f_sum = []
        for i in dup_lst:
            f_sum = []
            for path in i:
                check_sum = md5hex(path)
                f_sum.append(check_sum)
                f_sum.append(path)
            lst_f_sum.append(f_sum)
        return lst_f_sum

    def search_in_list_of_list(self, lst):
        for in_lst in lst:
            self.search_in_sum_list(in_lst)

    def search_in_sum_list(self, lst):
        """sum list - list with 0-element it's sum, 1-element it's fname
        """
        m_lst = lst[:]
        for i, _ in enumerate(lst):
            if not i % 2:
                fsum = lst[i]
            else:
                dup_lst = self.search_sum_in_sum_list(fsum, m_lst)
                if len(dup_lst) > 1:
                    self.flist_add(dup_lst)

    @staticmethod
    def search_sum_in_sum_list(fsum, lst):
        res_lst = []
        l_lst = lst[:]
        index = 0
        for i, _ in enumerate(l_lst):
            if not i % 2:
                if fsum == l_lst[i]:
                    fname = l_lst[i+1]
                    del lst[index]
                    del lst[index]
                    res_lst.append(fname)
                else:
                    index += 2
        return res_lst

    @staticmethod
    def date2string():
        return datetime.strftime(datetime.now(), '%Y-%m-%d--%H-%M-%S')

    @staticmethod
    def calc_files_in_directory(directory):
        i = 0
        for root, dirs, files in os.walk(directory):
            i += len(files)
        return i


class Progress(ProgressBar):
    """Manage Progress bar
    """
    def __init__(self):
        super(Progress, self).__init__()

    def msg_files(self, files):
        msg = " search in: %s files" % files
        self.set_bar_message(msg)

    def msg_files_in_files(self, files1, files2):
        msg = " search in: %s/%s files" % (files1, files2)
        self.set_bar_message(msg)
