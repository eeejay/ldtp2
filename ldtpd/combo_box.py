'''
LDTP v2 Core Combo box.

@author: Eitan Isaacson <eitan@ascender.com>
@author: Nagappan Alagappan <nagappan@gmail.com>
@copyright: Copyright (c) 2009 Eitan Isaacson
@copyright: Copyright (c) 2009 Nagappan Alagappan
@license: LGPL

http://ldtp.freedesktop.org

This file may be distributed and/or modified under the terms of the GNU General
Public License version 2 as published by the Free Software Foundation. This file
is distributed without any warranty; without even the implied warranty of 
merchantability or fitness for a particular purpose.

See "COPYING" in the source distribution for more information.

Headers in this file shall remain intact.
'''

import pyatspi 
from utils import Utils
from server_exception import LdtpServerException

class ComboBox(Utils):
    def selectitem(self, window_name, object_name, item_name):
        '''
        Select combo box item
        
        @param window_name: Window name to type in, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to type in, either full name,
        LDTP's name convention, or a Unix glob. 
        @type object_name: string
        @param item_name: Item name to select
        @type object_name: string

        @return: 1 on success.
        @rtype: integer
        '''
        obj = self._get_object(window_name, object_name)
        self._grab_focus(obj)

        child_obj = self._get_combo_child_object_type(obj)
        if not child_obj:
            raise LdtpServerException('Unable to get combo box children')
        if child_obj.getRole() == pyatspi.ROLE_LIST:
            index = 0
            for child in self._list_objects (child_obj):
                if child == child_obj:
                    # As the _list_objects gives the current object as well
                    # ignore it
                    continue
                try:
                    texti = child.queryText()
                    text = texti.getText(0, texti.characterCount)
                except NotImplementedError:
                    text = child.name

                if self._glob_match(item_name, text):
                    selectioni = child_obj.querySelection()
                    selectioni.selectChild(index)
                    try:
                        # If click action is available, then do it
                        self._click_object(child)
                    except:
                        # Incase of exception, just ignore it
                        pass
                    finally:
                        return 1
                index += 1
        elif child_obj.getRole() == pyatspi.ROLE_MENU:
            for child in self._list_objects (child_obj):
                if child == child_obj:
                    # As the _list_objects gives the current object as well
                    # ignore it
                    continue
                if self._glob_match(item_name, child.name):
                    self._click_object(child)
                    return 1
        raise LdtpServerException('Unable to select item')
    comboselect = selectitem

    def selectindex(self, window_name, object_name, item_index):
        '''
        Select combo box item based on index
        
        @param window_name: Window name to type in, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to type in, either full name,
        LDTP's name convention, or a Unix glob. 
        @type object_name: string
        @param item_index: Item index to select
        @type object_name: integer

        @return: 1 on success.
        @rtype: integer
        '''
        obj = self._get_object(window_name, object_name)
        self._grab_focus(obj)

        child_obj = self._get_combo_child_object_type(obj)
        if not child_obj:
            raise LdtpServerException('Unable to get combo box children')
        if child_obj.getRole() == pyatspi.ROLE_LIST:
            selectioni = child_obj.querySelection()
            selectioni.selectChild(item_index)
            return 1
        elif child_obj.getRole() == pyatspi.ROLE_MENU:
            index = 0
            for child in self._list_objects (child_obj):
                if child == child_obj:
                    # As the _list_objects gives the current object as well
                    # ignore it
                    continue
                if index == item_index:
                    self._click_object(child)
                    return 1
                index += 1
        raise LdtpServerException('Unable to select item index')

    def getallitem(self, window_name, object_name):
        '''
        Select combo box item
        
        @param window_name: Window name to type in, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to type in, either full name,
        LDTP's name convention, or a Unix glob. 
        @type object_name: string

        @return: list of string on success.
        @rtype: list
        '''
        obj = self._get_object(window_name, object_name)
        self._grab_focus(obj)

        child_obj = self._get_combo_child_object_type(obj)
        if not child_obj:
            raise LdtpServerException('Unable to get combo box children')
        item_list = []
        if child_obj.getRole() == pyatspi.ROLE_LIST:
            for child in self._list_objects (child_obj):
                if child == child_obj:
                    # As the _list_objects gives the current object as well
                    # ignore it
                    continue
                try:
                    texti = child.queryText()
                    text = texti.getText(0, texti.characterCount)
                except NotImplementedError:
                    text = child.name

                item_list.append(text)
            return item_list
        elif child_obj.getRole() == pyatspi.ROLE_MENU:
            for child in self._list_objects (child_obj):
                if child == child_obj:
                    # As the _list_objects gives the current object as well
                    # ignore it
                    continue
                if child.name and child.name != '':
                    item_list.append(child.name)
            return item_list
        raise LdtpServerException('Unable to select item')

    def showlist(self, window_name, object_name):
        '''
        Show combo box list / menu
        
        @param window_name: Window name to type in, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to type in, either full name,
        LDTP's name convention, or a Unix glob. 
        @type object_name: string

        @return: 1 on success.
        @rtype: integer
        '''
        obj = self._get_object(window_name, object_name)
        self._grab_focus(obj)

        child_obj = self._get_combo_child_object_type(obj)
        if not child_obj:
            raise LdtpServerException('Unable to get combo box children')

        if not self._check_state(obj, pyatspi.STATE_VISIBLE):
            self._click_object(obj, 'press')

        return 1

    def hidelist(self, window_name, object_name):
        '''
        Hide combo box list / menu
        
        @param window_name: Window name to type in, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to type in, either full name,
        LDTP's name convention, or a Unix glob. 
        @type object_name: string

        @return: 1 on success.
        @rtype: integer
        '''
        obj = self._get_object(window_name, object_name)
        self._grab_focus(obj)

        child_obj = self._get_combo_child_object_type(obj)
        if not child_obj:
            raise LdtpServerException('Unable to get combo box children')

        if self._check_state(obj, pyatspi.STATE_VISIBLE):
            self._click_object(obj, 'press')

        return 1

    def verifydropdown(self, window_name, object_name):
        '''
        Verify drop down list / menu poped up
        
        @param window_name: Window name to type in, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to type in, either full name,
        LDTP's name convention, or a Unix glob. 
        @type object_name: string

        @return: 1 on success.
        @rtype: integer
        '''
        obj = self._get_object(window_name, object_name)
        self._grab_focus(obj)

        child_obj = self._get_combo_child_object_type(obj)
        if not child_obj:
            raise LdtpServerException('Unable to get combo box children')

        if child_obj == pyatspi.ROLE_LIST and \
                self._check_state(obj, pyatspi.STATE_FOCUSABLE):
                return 1
        elif child_obj == pyatspi.ROLE_MENU:
            if self._check_state(obj, pyatspi.STATE_VISIBLE) and \
                    self._check_state(obj, pyatspi.STATE_SHOWING):
                return 1
        return 0

    def verifyshowlist(self, window_name, object_name):
        '''
        Verify drop down list / menu poped up
        
        @param window_name: Window name to type in, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to type in, either full name,
        LDTP's name convention, or a Unix glob. 
        @type object_name: string

        @return: 1 on success.
        @rtype: integer
        '''
        return self.verifydropdown(window_name, object_name)

    def verifyhidelist(self, window_name, object_name):
        '''
        Verify list / menu is hidden in combo box
        
        @param window_name: Window name to type in, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to type in, either full name,
        LDTP's name convention, or a Unix glob. 
        @type object_name: string

        @return: 1 on success.
        @rtype: integer
        '''
        obj = self._get_object(window_name, object_name)
        self._grab_focus(obj)

        child_obj = self._get_combo_child_object_type(obj)
        if not child_obj:
            raise LdtpServerException('Unable to get combo box children')

        if child_obj == pyatspi.ROLE_LIST and \
                not self._check_state(obj, pyatspi.STATE_FOCUSABLE):
                return 1
        elif child_obj == pyatspi.ROLE_MENU:
            if not self._check_state(obj, pyatspi.STATE_VISIBLE) and \
                    not self._check_state(obj, pyatspi.STATE_SHOWING):
                return 1
        return 0

    def verifyselect(self, window_name, object_name, item_name):
        '''
        Verify the item selected in combo box
        
        @param window_name: Window name to type in, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to type in, either full name,
        LDTP's name convention, or a Unix glob. 
        @type object_name: string
        @param item_name: Item name to select
        @type object_name: string

        @return: 1 on success.
        @rtype: integer
        '''
        obj = self._get_object(window_name, object_name)
        self._grab_focus(obj)

        child_obj = self._get_combo_child_object_type(obj)
        if not child_obj:
            raise LdtpServerException('Unable to get combo box children')
        if child_obj.getRole() == pyatspi.ROLE_LIST:
            for child in self._list_objects (child_obj):
                if child == child_obj:
                    # As the _list_objects gives the current object as well
                    # ignore it
                    continue
                try:
                    texti = child.queryText()
                    text = texti.getText(0, texti.characterCount)
                except NotImplementedError:
                    text = child.name

                if self._glob_match(item_name, text):
                    return 1
        elif child_obj.getRole() == pyatspi.ROLE_MENU:
            for child in self._list_objects (child_obj):
                if child == child_obj:
                    # As the _list_objects gives the current object as well
                    # ignore it
                    continue
                if self._glob_match(item_name, child.name):
                    return 1
        return 0
