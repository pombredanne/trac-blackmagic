from trac.core import Component, implements, TracError
from trac.config import Option, IntOption, ListOption, BoolOption
from trac.web.chrome import ITemplateProvider, add_stylesheet, add_script
from pkg_resources import resource_filename
from trac.web.api import ITemplateStreamFilter
from genshi.builder import tag
from genshi.core import Markup
from genshi.filters.transform import Transformer
import re, cPickle
from trac.perm import IPermissionRequestor

def istrue(v, otherwise=None):
    if v.lower() in ('yes', 'true', '1', 'on'):
        return True
    else:
        if otherwise is None:
            return False
        else:
            return otherwise

class TicketTweaks(Component):
    implements(ITemplateStreamFilter, ITemplateProvider, IPermissionRequestor)
    
    permissions = ListOption('blackmagic', 'permissions', [])
    gray_disabled = Option('blackmagic', 'gray_disabled', '', 
        doc="""If not set, disabled items will have their label striked through. 
        Otherwise, this color will be used to gray them out. Suggested #cccccc.""")
    ## IPermissionRequestor methods
    
    def get_permission_actions(self):
        return (x.upper() for x in self.permissions)
    
    ## ITemplateStreamFilter
    
    def filter_stream(self, req, method, filename, stream, data):
        if filename == "ticket.html":
            ##Check Permissions
            enchants = self.config.get('blackmagic', 'tweaks', '')
            for field in (x.strip() for x in enchants.split(',')):
                self.env.log.debug("Checking %s:" % field)
                disabled = False
                hidden = False
                #Get a list of the permissions from the config, split them on commas and remove spaces
                perms = self.config.get('blackmagic', '%s.permission' % field, '').upper()
                #Default to not having permissions
                hasPerm = True
                if perms:
                    hasPerm = False
                    #If there are permissions
                    self.env.log.debug("perm: %s" % len(perms))
                    perms = perms.split(',')
                    #walk the list we got back and check the request for the permission
                    for perm in perms:
                        perm = perm.strip()
                        self.env.log.debug("Checking perm: %s" % perm)
                        if perm in req.perm:
                            self.env.log.debug("User has perm: %s" % perm)
                            hasPerm = True
                    if hasPerm == False:
                        denial = self.config.get('blackmagic', '%s.ondenial' % field, None)
                        if denial:
                            if denial == "disable":
                                disabled = True
                            elif denial == "hide":
                                hidden = True
                            else:
                                disabled = True
                        else:
                            disabled = True

                self.env.log.debug('hasPerm: %s' % hasPerm)
                if hidden == False:
                    if self.config.get('blackmagic', '%s.label' % field, None):
                        labelTXT = self.config.get('blackmagic', '%s.label' % field)
                        label = tag.label("%s:" %labelTXT, for_="field-%s" % field)
                        stream = stream | Transformer('//label[@for="field-%s"]' % field).replace(label)

                if hasPerm == False:   
                    if istrue(self.config.get('blackmagic', '%s.hide' % field, None)):
                        hidden = True
                        
                    if disabled or istrue(self.config.get('blackmagic', '%s.disable' % field, False)):
                        stream = stream | Transformer('//*[@id="field-%s"]' % field).attr("disabled", "disabled")
                        label = self.config.get('blackmagic', '%s.label' % field)
                        if not label:
                            label = field.capitalize()
                        if not self.gray_disabled:
                            stream = stream | Transformer('//label[@for="field-%s"]' % field).replace(
                                tag.strike()('%s:' % label)
                            )
                        else:
                            stream = stream | Transformer('//label[@for="field-%s"]' % field).replace(
                                tag.span(style="color:%s" % self.gray_disabled)('%s:' % label)
                            )
                    
                    if hidden or istrue(self.config.get('blackmagic', '%s.hide' % field, None)):
                        stream = stream | Transformer('//th[@id="h_%s"]' % field).replace(" ") 
                        stream = stream | Transformer('//td[@headers="h_%s"]' % field).replace(" ")
                        stream = stream | Transformer('//label[@for="field-%s"]' % field).replace(" ")
                        stream = stream | Transformer('//*[@id="field-%s"]' % field).replace(" ")

                    
                if hidden == False:
                    if self.config.get('blackmagic', '%s.notice' % field, None):
                        stream = stream | Transformer('//*[@id="field-%s"]' % field).after(
                            tag.br() + tag.small(class_="notice-%s" %field)(
                                tag.em()(
                                    Markup(self.config.get('blackmagic', '%s.notice' % field))
                                )
                            )
                        )
                    
                tip = self.config.get('blackmagic', '%s.tip' % field, None)
                if tip:
                    stream = stream | Transformer('//div[@id="banner"]').before(
                        tag.script(type="text/javascript", 
                        src=req.href.chrome("blackmagic", "js", "wz_tooltip.js"))()
                    )
                    
                    stream = stream | Transformer('//*[@id="field-%s"]' % field).attr(
                        "onmouseover", "Tip('%s')" % tip.replace(r"'", r"\'")
                    )
                        
                    
        return stream

    ## ITemplateProvider

    def get_htdocs_dirs(self):
        from pkg_resources import resource_filename
        return [('blackmagic', resource_filename(__name__, 'htdocs'))]
          
    def get_templates_dirs(self):
        return []    
