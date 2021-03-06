'''
LDTP v2 Core.

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

import re
import pyatspi 
from utils import Utils

class Menu(Utils):
    def selectmenuitem(self, window_name, object_name):
        '''
        Select (click) a menu item.
        
        @param window_name: Window name to look for, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to look for, either full name,
        LDTP's name convention, or a Unix glob. Or menu heirarchy
        @type object_name: string

        @return: 1 on success.
        @rtype: integer
        '''
        if re.search(';', object_name):
            obj = self._get_menu_hierarchy(window_name, object_name)
        else:
            obj = self._get_object(window_name, object_name)

        self._click_object(obj)

        return 1

    def doesmenuitemexist(self, window_name, object_name):
        '''
        Check a menu item exist.
        
        @param window_name: Window name to look for, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to look for, either full name,
        LDTP's name convention, or a Unix glob. Or menu heirarchy
        @type object_name: string

        @return: 1 on success.
        @rtype: integer
        '''
        try:
            if re.search(';', object_name):
                obj = self._get_menu_hierarchy(window_name, object_name)
            else:
                obj = self._get_object(window_name, object_name)
            return 1
        except:
            return 0

    def listsubmenus(self, window_name, object_name):
        '''
        List children of menu item
        
        @param window_name: Window name to look for, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to look for, either full name,
        LDTP's name convention, or a Unix glob. Or menu heirarchy
        @type object_name: string

        @return: menu item in ';' separated format on success.
        @rtype: string
        '''
        if re.search(';', object_name):
            obj = self._get_menu_hierarchy(window_name, object_name)
        else:
            obj = self._get_object(window_name, object_name)
        _children = ''
        for _child in self._list_objects(obj):
            if _child.name == '' or _child.name == 'Empty' or \
                    obj == _child:
                # If empty string don't add it to the list or
                # if the given object and child object matches
                continue
            if _children == '':
                _children += _child.name
            else:
                _children += ';%s' % _child.name
        return _children

    def menucheck(self, window_name, object_name):
        '''
        Check (click) a menu item.
        
        @param window_name: Window name to look for, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to look for, either full name,
        LDTP's name convention, or a Unix glob. Or menu heirarchy
        @type object_name: string

        @return: 1 on success.
        @rtype: integer
        '''
        if re.search(';', object_name):
            obj = self._get_menu_hierarchy(window_name, object_name)
        else:
            obj = self._get_object(window_name, object_name)

        if self._check_state(obj, pyatspi.STATE_CHECKED) == False:
            self._click_object(obj)

        return 1

    def menuuncheck(self, window_name, object_name):
        '''
        Check (click) a menu item.
        
        @param window_name: Window name to look for, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to look for, either full name,
        LDTP's name convention, or a Unix glob. Or menu heirarchy
        @type object_name: string

        @return: 1 on success.
        @rtype: integer
        '''
        if re.search(';', object_name):
            obj = self._get_menu_hierarchy(window_name, object_name)
        else:
            obj = self._get_object(window_name, object_name)

        if self._check_state(obj, pyatspi.STATE_CHECKED):
            self._click_object(obj)

        return 1

    def invokemenu(self, window_name, object_name):
        '''
        Invoke menu item.
        
        @param window_name: Window name to look for, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to look for, either full name,
        LDTP's name convention, or a Unix glob. 
        @type object_name: string

        @return: 1 on success.
        @rtype: integer
        '''
        return self.press (window_name, object_name)

