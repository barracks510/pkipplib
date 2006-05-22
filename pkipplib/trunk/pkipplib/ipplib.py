#! /usr/bin/env python
# -*- coding: ISO-8859-15 -*-
#
# pkipplib : IPP and CUPS support for Python
#
# (c) 2003, 2004, 2005, 2006 Jerome Alet <alet@librelogiciel.com>
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# $Id$
#
#

import sys
import urllib2
from struct import pack, unpack

IPP_VERSION = "1.1"     # default version number

IPP_PORT = 631

IPP_MAX_NAME = 256
IPP_MAX_VALUES = 8

IPP_TAG_ZERO = 0x00
IPP_TAG_OPERATION = 0x01
IPP_TAG_JOB = 0x02
IPP_TAG_END = 0x03
IPP_TAG_PRINTER = 0x04
IPP_TAG_UNSUPPORTED_GROUP = 0x05
IPP_TAG_SUBSCRIPTION = 0x06
IPP_TAG_EVENT_NOTIFICATION = 0x07
IPP_TAG_UNSUPPORTED_VALUE = 0x10
IPP_TAG_DEFAULT = 0x11
IPP_TAG_UNKNOWN = 0x12
IPP_TAG_NOVALUE = 0x13
IPP_TAG_NOTSETTABLE = 0x15
IPP_TAG_DELETEATTR = 0x16
IPP_TAG_ADMINDEFINE = 0x17
IPP_TAG_INTEGER = 0x21
IPP_TAG_BOOLEAN = 0x22
IPP_TAG_ENUM = 0x23
IPP_TAG_STRING = 0x30
IPP_TAG_DATE = 0x31
IPP_TAG_RESOLUTION = 0x32
IPP_TAG_RANGE = 0x33
IPP_TAG_BEGIN_COLLECTION = 0x34
IPP_TAG_TEXTLANG = 0x35
IPP_TAG_NAMELANG = 0x36
IPP_TAG_END_COLLECTION = 0x37
IPP_TAG_TEXT = 0x41
IPP_TAG_NAME = 0x42
IPP_TAG_KEYWORD = 0x44
IPP_TAG_URI = 0x45
IPP_TAG_URISCHEME = 0x46
IPP_TAG_CHARSET = 0x47
IPP_TAG_LANGUAGE = 0x48
IPP_TAG_MIMETYPE = 0x49
IPP_TAG_MEMBERNAME = 0x4a
IPP_TAG_MASK = 0x7fffffff
IPP_TAG_COPY = -0x7fffffff-1

IPP_RES_PER_INCH = 3
IPP_RES_PER_CM = 4

IPP_FINISHINGS_NONE = 3
IPP_FINISHINGS_STAPLE = 4
IPP_FINISHINGS_PUNCH = 5
IPP_FINISHINGS_COVER = 6
IPP_FINISHINGS_BIND = 7
IPP_FINISHINGS_SADDLE_STITCH = 8
IPP_FINISHINGS_EDGE_STITCH = 9
IPP_FINISHINGS_FOLD = 10
IPP_FINISHINGS_TRIM = 11
IPP_FINISHINGS_BALE = 12
IPP_FINISHINGS_BOOKLET_MAKER = 13
IPP_FINISHINGS_JOB_OFFSET = 14
IPP_FINISHINGS_STAPLE_TOP_LEFT = 20
IPP_FINISHINGS_STAPLE_BOTTOM_LEFT = 21
IPP_FINISHINGS_STAPLE_TOP_RIGHT = 22
IPP_FINISHINGS_STAPLE_BOTTOM_RIGHT = 23
IPP_FINISHINGS_EDGE_STITCH_LEFT = 24
IPP_FINISHINGS_EDGE_STITCH_TOP = 25
IPP_FINISHINGS_EDGE_STITCH_RIGHT = 26
IPP_FINISHINGS_EDGE_STITCH_BOTTOM = 27
IPP_FINISHINGS_STAPLE_DUAL_LEFT = 28
IPP_FINISHINGS_STAPLE_DUAL_TOP = 29
IPP_FINISHINGS_STAPLE_DUAL_RIGHT = 30
IPP_FINISHINGS_STAPLE_DUAL_BOTTOM = 31
IPP_FINISHINGS_BIND_LEFT = 50
IPP_FINISHINGS_BIND_TOP = 51
IPP_FINISHINGS_BIND_RIGHT = 52
IPP_FINISHINGS_BIND_BOTTO = 53

IPP_PORTRAIT = 3
IPP_LANDSCAPE = 4
IPP_REVERSE_LANDSCAPE = 5
IPP_REVERSE_PORTRAIT = 6

IPP_QUALITY_DRAFT = 3
IPP_QUALITY_NORMAL = 4
IPP_QUALITY_HIGH = 5

IPP_JOB_PENDING = 3
IPP_JOB_HELD = 4
IPP_JOB_PROCESSING = 5
IPP_JOB_STOPPED = 6
IPP_JOB_CANCELLED = 7
IPP_JOB_ABORTED = 8
IPP_JOB_COMPLETE = 9

IPP_PRINTER_IDLE = 3
IPP_PRINTER_PROCESSING = 4
IPP_PRINTER_STOPPED = 5

IPP_ERROR = -1
IPP_IDLE = 0
IPP_HEADER = 1
IPP_ATTRIBUTE = 2
IPP_DATA = 3

IPP_PRINT_JOB = 0x0002
IPP_PRINT_URI = 0x0003
IPP_VALIDATE_JOB = 0x0004
IPP_CREATE_JOB = 0x0005
IPP_SEND_DOCUMENT = 0x0006
IPP_SEND_URI = 0x0007
IPP_CANCEL_JOB = 0x0008
IPP_GET_JOB_ATTRIBUTES = 0x0009
IPP_GET_JOBS = 0x000a
IPP_GET_PRINTER_ATTRIBUTES = 0x000b
IPP_HOLD_JOB = 0x000c
IPP_RELEASE_JOB = 0x000d
IPP_RESTART_JOB = 0x000e
IPP_PAUSE_PRINTER = 0x0010
IPP_RESUME_PRINTER = 0x0011
IPP_PURGE_JOBS = 0x0012
IPP_SET_PRINTER_ATTRIBUTES = 0x0013
IPP_SET_JOB_ATTRIBUTES = 0x0014
IPP_GET_PRINTER_SUPPORTED_VALUES = 0x0015
IPP_CREATE_PRINTER_SUBSCRIPTION = 0x0016
IPP_CREATE_JOB_SUBSCRIPTION = 0x0017
IPP_GET_SUBSCRIPTION_ATTRIBUTES = 0x0018
IPP_GET_SUBSCRIPTIONS = 0x0019
IPP_RENEW_SUBSCRIPTION = 0x001a
IPP_CANCEL_SUBSCRIPTION = 0x001b
IPP_GET_NOTIFICATIONS = 0x001c
IPP_SEND_NOTIFICATIONS = 0x001d
IPP_GET_PRINT_SUPPORT_FILES = 0x0021
IPP_ENABLE_PRINTER = 0x0022
IPP_DISABLE_PRINTER = 0x0023
IPP_PAUSE_PRINTER_AFTER_CURRENT_JOB = 0x0024
IPP_HOLD_NEW_JOBS = 0x0025
IPP_RELEASE_HELD_NEW_JOBS = 0x0026
IPP_DEACTIVATE_PRINTER = 0x0027
IPP_ACTIVATE_PRINTER = 0x0028
IPP_RESTART_PRINTER = 0x0029
IPP_SHUTDOWN_PRINTER = 0x002a
IPP_STARTUP_PRINTER = 0x002b
IPP_REPROCESS_JOB = 0x002c
IPP_CANCEL_CURRENT_JOB = 0x002d
IPP_SUSPEND_CURRENT_JOB = 0x002e
IPP_RESUME_JOB = 0x002f
IPP_PROMOTE_JOB = 0x0030
IPP_SCHEDULE_JOB_AFTER = 0x0031
IPP_PRIVATE = 0x4000
CUPS_GET_DEFAULT = 0x4001
CUPS_GET_PRINTERS = 0x4002
CUPS_ADD_PRINTER = 0x4003
CUPS_DELETE_PRINTER = 0x4004
CUPS_GET_CLASSES = 0x4005
CUPS_ADD_CLASS = 0x4006
CUPS_DELETE_CLASS = 0x4007
CUPS_ACCEPT_JOBS = 0x4008
CUPS_REJECT_JOBS = 0x4009
CUPS_SET_DEFAULT = 0x400a
CUPS_GET_DEVICES = 0x400b
CUPS_GET_PPDS = 0x400c
CUPS_MOVE_JOB = 0x400d
CUPS_AUTHENTICATE_JOB = 0x400e

IPP_OK = 0x0000
IPP_OK_SUBST = 0x0001
IPP_OK_CONFLICT = 0x0002
IPP_OK_IGNORED_SUBSCRIPTIONS = 0x0003
IPP_OK_IGNORED_NOTIFICATIONS = 0x0004
IPP_OK_TOO_MANY_EVENTS = 0x0005
IPP_OK_BUT_CANCEL_SUBSCRIPTION = 0x0006
IPP_REDIRECTION_OTHER_SITE = 0x0300
IPP_BAD_REQUEST = 0x0400
IPP_FORBIDDEN = 0x0401
IPP_NOT_AUTHENTICATED = 0x0402
IPP_NOT_AUTHORIZED = 0x0403
IPP_NOT_POSSIBLE = 0x0404
IPP_TIMEOUT = 0x0405
IPP_NOT_FOUND = 0x0406
IPP_GONE = 0x0407
IPP_REQUEST_ENTITY = 0x0408
IPP_REQUEST_VALUE = 0x0409
IPP_DOCUMENT_FORMAT = 0x040a
IPP_ATTRIBUTES = 0x040b
IPP_URI_SCHEME = 0x040c
IPP_CHARSET = 0x040d
IPP_CONFLICT = 0x040e
IPP_COMPRESSION_NOT_SUPPORTED = 0x040f
IPP_COMPRESSION_ERROR = 0x0410
IPP_DOCUMENT_FORMAT_ERROR = 0x0411
IPP_DOCUMENT_ACCESS_ERROR = 0x0412
IPP_ATTRIBUTES_NOT_SETTABLE = 0x0413
IPP_IGNORED_ALL_SUBSCRIPTIONS = 0x0414
IPP_TOO_MANY_SUBSCRIPTIONS = 0x0415
IPP_IGNORED_ALL_NOTIFICATIONS = 0x0416
IPP_PRINT_SUPPORT_FILE_NOT_FOUND = 0x0417

IPP_INTERNAL_ERROR = 0x0500
IPP_OPERATION_NOT_SUPPORTED = 0x0501
IPP_SERVICE_UNAVAILABLE = 0x0502
IPP_VERSION_NOT_SUPPORTED = 0x0503
IPP_DEVICE_ERROR = 0x0504
IPP_TEMPORARY_ERROR = 0x0505
IPP_NOT_ACCEPTING = 0x0506
IPP_PRINTER_BUSY = 0x0507
IPP_ERROR_JOB_CANCELLED = 0x0508
IPP_MULTIPLE_JOBS_NOT_SUPPORTED = 0x0509
IPP_PRINTER_IS_DEACTIVATED = 0x50a
  
class IPPError(Exception) :
    """An exception for IPP related stuff."""
    def __init__(self, message = ""):
        self.message = message
        Exception.__init__(self, message)
    def __repr__(self):
        return self.message
    __str__ = __repr__

class FakeAttribute :
    """Fakes an IPPRequest attribute to simplify usage syntax."""
    def __init__(self, request, name) :
        """Initializes the fake attribute."""
        self.request = request
        self.name = name
        
    def __setitem__(self, key, value) :
        """Appends the value to the real attribute."""
        attributeslist = getattr(self.request, "_%s_attributes" % self.name)
        for i in range(len(attributeslist)) :
            attribute = attributeslist[i]
            for j in range(len(attribute)) :
                (attrname, attrvalue) = attribute[j]
                if attrname == key :
                    attribute[j][1].append(value)
                    return
            attribute.append((key, [value]))        
            
    def __getitem__(self, key) :
        """Returns an attribute's value."""
        attributeslist = getattr(self.request, "_%s_attributes" % self.name)
        for i in range(len(attributeslist)) :
            attribute = attributeslist[i]
            for j in range(len(attribute)) :
                (attrname, attrvalue) = attribute[j]
                if attrname == key :
                    return attrvalue
        raise KeyError, key            
    
class IPPRequest :
    """A class for IPP requests."""
    attributes_types = ("operation", "job", "printer", "unsupported", \
                                     "subscription", "event_notification")
    def __init__(self, data="", version=IPP_VERSION, 
                                operation_id=None, \
                                request_id=None, \
                                url = "http://localhost:631", \
                                username = None, \
                                password = None, \
                                debug=False) :
        """Initializes an IPP Message object.
        
           Parameters :
           
             data : the complete IPP Message's content.
             debug : a boolean value to output debug info on stderr.
        """
        self.url = url
        self.username = username
        self.password = password
        self.debug = debug
        self._data = data
        self.parsed = False
        
        # Initializes message
        self.setVersion(version)                
        self.setOperationId(operation_id)
        self.setRequestId(request_id)
        self.data = ""
        
        for attrtype in self.attributes_types :
            setattr(self, "_%s_attributes" % attrtype, [[]])
        
        # Initialize tags    
        self.tags = [ None ] * 256 # by default all tags reserved
        
        # Delimiter tags
        self.tags[0x01] = "operation-attributes-tag"
        self.tags[0x02] = "job-attributes-tag"
        self.tags[0x03] = "end-of-attributes-tag"
        self.tags[0x04] = "printer-attributes-tag"
        self.tags[0x05] = "unsupported-attributes-tag"
        self.tags[0x06] = "subscription-attributes-tag"
        self.tags[0x07] = "event-notification-attributes-tag"
        
        # out of band values
        self.tags[0x10] = "unsupported"
        self.tags[0x11] = "reserved-for-future-default"
        self.tags[0x12] = "unknown"
        self.tags[0x13] = "no-value"
        self.tags[0x15] = "not-settable"
        self.tags[0x16] = "delete-attribute"
        self.tags[0x17] = "admin-define"
  
        # integer values
        self.tags[0x20] = "generic-integer"
        self.tags[0x21] = "integer"
        self.tags[0x22] = "boolean"
        self.tags[0x23] = "enum"
        
        # octetString
        self.tags[0x30] = "octetString-with-an-unspecified-format"
        self.tags[0x31] = "dateTime"
        self.tags[0x32] = "resolution"
        self.tags[0x33] = "rangeOfInteger"
        self.tags[0x34] = "begCollection" # TODO : find sample files for testing
        self.tags[0x35] = "textWithLanguage"
        self.tags[0x36] = "nameWithLanguage"
        self.tags[0x37] = "endCollection"
        
        # character strings
        self.tags[0x40] = "generic-character-string"
        self.tags[0x41] = "textWithoutLanguage"
        self.tags[0x42] = "nameWithoutLanguage"
        self.tags[0x44] = "keyword"
        self.tags[0x45] = "uri"
        self.tags[0x46] = "uriScheme"
        self.tags[0x47] = "charset"
        self.tags[0x48] = "naturalLanguage"
        self.tags[0x49] = "mimeMediaType"
        self.tags[0x4a] = "memberAttrName"
        
        # Reverse mapping to generate IPP messages
        self.tagvalues = {}
        for i in range(len(self.tags)) :
            value = self.tags[i]
            if value is not None :
                self.tagvalues[value] = i
                                     
    def __getattr__(self, name) :                                 
        """Fakes attribute access."""
        if name in self.attributes_types :
            return FakeAttribute(self, name)
        else :
            raise AttributeError, name
            
    def __str__(self) :        
        """Returns the parsed IPP message in a readable form."""
        if not self.parsed :
            return ""
        mybuffer = []
        mybuffer.append("IPP version : %s.%s" % self.version)
        mybuffer.append("IPP operation Id : 0x%04x" % self.operation_id)
        mybuffer.append("IPP request Id : 0x%08x" % self.request_id)
        for attrtype in self.attributes_types :
            for attribute in getattr(self, "_%s_attributes" % attrtype) :
                if attribute :
                    mybuffer.append("%s attributes :" % attrtype.title())
                for (name, value) in attribute :
                    mybuffer.append("  %s : %s" % (name, value))
        if self.data :            
            mybuffer.append("IPP datas : %s" % repr(self.data))
        return "\n".join(mybuffer)
        
    def logDebug(self, msg) :    
        """Prints a debug message."""
        if self.debug :
            sys.stderr.write("%s\n" % msg)
            sys.stderr.flush()
            
    def setVersion(self, version) :
        """Sets the request's operation id."""
        if version is not None :
            try :
                self.version = [int(p) for p in version.split(".")]
            except AttributeError :
                if len(version) == 2 : # 2-tuple
                    self.version = version
                else :    
                    try :
                        self.version = [int(p) for p in str(float(version)).split(".")]
                    except :
                        self.version = [int(p) for p in IPP_VERSION.split(".")]
        
    def setOperationId(self, opid) :        
        """Sets the request's operation id."""
        self.operation_id = opid
        
    def setRequestId(self, reqid) :        
        """Sets the request's request id."""
        self.request_id = reqid
        
    def nextRequestId(self) :        
        """Increments the current request id and returns the new value."""
        try :
            self.request_id += 1
        except TypeError :    
            self.request_id = 1
        return self.request_id
            
    def dump(self) :    
        """Generates an IPP Message.
        
           Returns the message as a string of text.
        """    
        mybuffer = []
        if None not in (self.version, self.operation_id) :
            if self.request_id is None :
                self.nextRequestId()
            mybuffer.append(chr(self.version[0]) + chr(self.version[1]))
            mybuffer.append(pack(">H", self.operation_id))
            mybuffer.append(pack(">I", self.request_id))
            for attrtype in self.attributes_types :
                for attribute in getattr(self, "_%s_attributes" % attrtype) :
                    if attribute :
                        mybuffer.append(chr(self.tagvalues["%s-attributes-tag" % attrtype]))
                    for (attrname, value) in attribute :
                        nameprinted = 0
                        for (vtype, val) in value :
                            mybuffer.append(chr(self.tagvalues[vtype]))
                            if not nameprinted :
                                mybuffer.append(pack(">H", len(attrname)))
                                mybuffer.append(attrname)
                                nameprinted = 1
                            else :     
                                mybuffer.append(pack(">H", 0))
                            if vtype in ("integer", "enum") :
                                mybuffer.append(pack(">H", 4))
                                mybuffer.append(pack(">I", val))
                            elif vtype == "boolean" :
                                mybuffer.append(pack(">H", 1))
                                mybuffer.append(chr(val))
                            else :    
                                mybuffer.append(pack(">H", len(val)))
                                mybuffer.append(val)
            mybuffer.append(chr(self.tagvalues["end-of-attributes-tag"]))
        mybuffer.append(self.data)    
        return "".join(mybuffer)
            
    def parse(self) :
        """Parses an IPP Request.
        
           NB : Only a subset of RFC2910 is implemented.
        """
        self._curname = None
        self._curattributes = None
        
        self.setVersion((ord(self._data[0]), ord(self._data[1])))
        self.setOperationId(unpack(">H", self._data[2:4])[0])
        self.setRequestId(unpack(">I", self._data[4:8])[0])
        self.position = 8
        endofattributes = self.tagvalues["end-of-attributes-tag"]
        maxdelimiter = self.tagvalues["event-notification-attributes-tag"]
        nulloffset = lambda : 0
        try :
            tag = ord(self._data[self.position])
            while tag != endofattributes :
                self.position += 1
                name = self.tags[tag]
                if name is not None :
                    func = getattr(self, name.replace("-", "_"), nulloffset)
                    self.position += func()
                    if ord(self._data[self.position]) > maxdelimiter :
                        self.position -= 1
                        continue
                oldtag = tag        
                tag = ord(self._data[self.position])
                if tag == oldtag :
                    self._curattributes.append([])
        except IndexError :
            raise IPPError, "Unexpected end of IPP message."
            
        self.data = self._data[self.position+1:]            
        self.parsed = True
        
    def parseTag(self) :    
        """Extracts information from an IPP tag."""
        pos = self.position
        tagtype = self.tags[ord(self._data[pos])]
        pos += 1
        posend = pos2 = pos + 2
        namelength = unpack(">H", self._data[pos:pos2])[0]
        if not namelength :
            name = self._curname
        else :    
            posend += namelength
            self._curname = name = self._data[pos2:posend]
        pos2 = posend + 2
        valuelength = unpack(">H", self._data[posend:pos2])[0]
        posend = pos2 + valuelength
        value = self._data[pos2:posend]
        if tagtype in ("integer", "enum") :
            value = unpack(">I", value)[0]
        elif tagtype == "boolean" :    
            value = ord(value)
        try :    
            (oldname, oldval) = self._curattributes[-1][-1]
            if oldname == name :
                oldval.append((tagtype, value))
            else :    
                raise IndexError
        except IndexError :    
            self._curattributes[-1].append((name, [(tagtype, value)]))
        self.logDebug("%s(%s) : %s" % (name, tagtype, value))
        return posend - self.position
        
    def operation_attributes_tag(self) : 
        """Indicates that the parser enters into an operation-attributes-tag group."""
        self._curattributes = self._operation_attributes
        return self.parseTag()
        
    def job_attributes_tag(self) : 
        """Indicates that the parser enters into a job-attributes-tag group."""
        self._curattributes = self._job_attributes
        return self.parseTag()
        
    def printer_attributes_tag(self) : 
        """Indicates that the parser enters into a printer-attributes-tag group."""
        self._curattributes = self._printer_attributes
        return self.parseTag()
        
    def unsupported_attributes_tag(self) : 
        """Indicates that the parser enters into an unsupported-attributes-tag group."""
        self._curattributes = self._unsupported_attributes
        return self.parseTag()
        
    def subscription_attributes_tag(self) : 
        """Indicates that the parser enters into a subscription-attributes-tag group."""
        self._curattributes = self._subscription_attributes
        return self.parseTag()
        
    def event_notification_attributes_tag(self) : 
        """Indicates that the parser enters into an event-notification-attributes-tag group."""
        self._curattributes = self._event_notification_attributes
        return self.parseTag()
        
    def doRequest(self, url=None, username=None, password=None, samerequestid=False) :
        """Sends the current request to the URL.
           NB : only ipp:// URLs are currently unsupported so use
           either http://host:631/ or https://host:443 instead...
           
           returns a new IPPRequest object, containing the parsed answer.
        """   
        if not samerequestid :
            self.nextRequestId()
        cx = urllib2.Request(url=url or self.url or "http://localhost:631/", 
                             data=self.dump())
        cx.add_header("Content-Type", "application/ipp")
        response = urllib2.urlopen(cx)
        datas = response.read()
        ippresponse = IPPRequest(datas)
        ippresponse.parse()
        return ippresponse
        
            
class CUPS :
    """A class for a CUPS instance."""
    def __init__(self, url="http://localhost:631", username=None, password=None, charset="utf-8", language="en-us") :
        """Initializes the CUPS instance."""
        self.url = url
        self.username = username
        self.password = password
        self.charset = charset
        self.language = language
        
    def identifierToURI(self, service, ident) :
        """Transforms an identifier into a particular URI depending on requested service."""
        return "%s/%s/%s" % (self.url.replace("http://", "ipp://"),
                             service,
                             ident)
        
    def newRequest(self, operationid=None) :
        """Generates a new empty request."""
        if operationid is not None :
            req = IPPRequest(operation_id=operationid, \
                             url=self.url, \
                             username=self.username, \
                             password=self.password)
            req.operation["attributes-charset"] = ("charset", self.charset)
            req.operation["attributes-natural-language"] = ("naturalLanguage", self.language)
            return req
    
    def getDefault(self) :
        """Retrieves CUPS' default printer."""
        return self.newRequest(CUPS_GET_DEFAULT).doRequest()
    
    def getJobAttributes(self, jobid) :    
        """Retrieves a print job's attributes."""
        req = self.newRequest(IPP_GET_JOB_ATTRIBUTES)
        req.operation["job-uri"] = ("uri", self.identifierToURI("jobs", jobid))
        return req.doRequest()
        
    def getPPD(self, queuename) :    
        """Retrieves the PPD for a particular queuename."""
        req = self.newRequest(IPP_GET_PRINTER_ATTRIBUTES)
        req.operation["printer-uri"] = ("uri", self.identifierToURI("printers", queuename))
        for attrib in ("printer-uri-supported", "printer-type", "member-uris") :
            req.operation["requested-attributes"] = ("nameWithoutLanguage", attrib)
        return req.doRequest()  # TODO : get the PPD from the actual print server
        
            
if __name__ == "__main__" :            
    if (len(sys.argv) < 2) or (sys.argv[1] == "--debug") :
        print "usage : python ipp.py /var/spool/cups/c00005 [--debug] (for example)\n"
    else :    
        infile = open(sys.argv[1], "rb")
        data = infile.read()
        infile.close()
        
        message = IPPRequest(data, debug=(sys.argv[-1]=="--debug"))
        message.parse()
        message2 = IPPRequest(message.dump())
        message2.parse()
        data2 = message2.dump()
        
        if data == data2 :
            print "Test OK : parsing original and parsing the output of the dump produce the same dump !"
            print str(message)
        else :    
            print "Test Failed !"
            print str(message)
            print
            print str(message2)
        
