from django.core.management import setup_environ
from django.template.loader import render_to_string

import settings
setup_environ(settings)

import os, sys
from domain.models import Site

import datetime, random, hashlib, time


# Port from "winning quick [site_name]"

# Important not change
def dbslug(SITE_NAME):
    return 'ow_' + SITE_NAME.replace('.', '_').replace('-', '_')[0:12]

def create(site):

    # Set state ====================================================
    site.status = site.BUILDING
    site.save()

    # 10% =====================
    site.percent = 10
    site.save()

    SITE_NAME    = site.name
    PACKAGE_CODE = site.package.code

    # openweb portal settings
    OW_USER     = settings.OW_USER     
    OW_APACHE   = settings.OW_APACHE   
    OW_PLATFORM = settings.OW_PLATFORM 
    OW_VHOST    = settings.OW_VHOST    
    OW_SITES    = settings.OW_SITES    
    OW_DOMAIN   = settings.OW_DOMAIN   
    DB          = settings.DATABASES

    if not OW_SITES or not OW_VHOST or not SITE_NAME:
        return False

    # create_site_dirs
    os.makedirs('%s%s'      % (OW_SITES, SITE_NAME), 0775)
    os.makedirs('%s%s/logs' % (OW_SITES, SITE_NAME), 0775)
    os.makedirs('%s%s/tmp'  % (OW_SITES, SITE_NAME), 0775)

    # 20% =====================
    site.percent = 20
    site.save()

    # create_virtual_host
    apache_vh = render_to_string('apache', locals())
    f = open('%s%s.%s' % (OW_VHOST, SITE_NAME, OW_DOMAIN), 'w')
    f.write(apache_vh)
    f.close()
    # 30% =====================
    site.percent = 30
    site.save()

    # create_database
    DB_NAME = DB_PASS = DB_USER = dbslug(SITE_NAME)
    DB_PASS = DB_PASS + hashlib.sha1(str(random.random())).hexdigest()[:5]
    CREATE_DB = "CREATE DATABASE %s DEFAULT CHARACTER SET 'utf8' DEFAULT COLLATE 'utf8_general_ci'" % DB_NAME
    GRANT_DB  = "GRANT ALL PRIVILEGES ON %s.* TO '%s'@'localhost' IDENTIFIED BY '%s'" % (DB_NAME, DB_USER, DB_PASS)
    SQL = 'mysql -u%s -p%s -e "%s;%s;"' % (DB['default']['USER'], DB['default']['PASSWORD'], CREATE_DB, GRANT_DB)
    os.system(SQL)
    
    site.dbname = DB_NAME
    site.dbuser = DB_USER
    site.dbpass = DB_PASS
    site.save()

    # 50% =====================
    site.percent = 50
    site.save()

    #copy_site
    os.system('cp -R %s%s/code %s%s/htdocs' % (OW_PLATFORM, PACKAGE_CODE, OW_SITES, SITE_NAME))

    conf = render_to_string('platforms/%s.php' % site.package.system, locals())
    cmap = {
        'wordpress': 'wp-config.php',
        'joomla': 'configuration.php',
        'drupal': 'sites/default/settings.php'
    }
    f = open('%s%s/htdocs/%s' % (OW_SITES, SITE_NAME, cmap[site.package.system]), 'w')
    f.write(conf)
    f.close()

    # 65% =====================
    site.percent = 65
    site.save()

    os.system('mysql -u%s -p%s %s < %s%s/db.sql' % (DB_USER, DB_PASS, DB_NAME, OW_PLATFORM, PACKAGE_CODE))

    # Set state ======================================================
    site.status = site.INITIAL
    site.save()

    # 80% =====================
    site.percent = 80
    site.save()

    # Avahi setiing 
    try:
        from avahi_alias import publish_cname

        publish_cname('%s.%s' % (SITE_NAME, OW_DOMAIN))
    except:
        pass


def delete(SITE_NAME):

    # openweb portal settings
    OW_USER     = settings.OW_USER     
    OW_APACHE   = settings.OW_APACHE   
    OW_PLATFORM = settings.OW_PLATFORM 
    OW_VHOST    = settings.OW_VHOST    
    OW_SITES    = settings.OW_SITES    
    OW_DOMAIN   = settings.OW_DOMAIN   
    DB          = settings.DATABASES

    if not OW_SITES or not OW_VHOST or not SITE_NAME:
        return False

    os.system('rm -rf %s%s'    % (OW_SITES, SITE_NAME))
    os.system('rm -rf %s%s.%s' % (OW_VHOST, SITE_NAME, OW_DOMAIN))

    DB_NAME = DB_USER = dbslug(SITE_NAME)
    #REVOKE_PRIV = "REVOKE ALL PRIVILEGES, GRANT OPTION FROM '%s'@'localhost'" % DB_USER
    DROP_USER   = "DROP USER '%s'@'localhost'" % DB_USER
    DROP_DB     = "DROP DATABASE %s" % DB_NAME
    SQL = 'mysql -u%s -p%s -e "%s;%s;"' % (DB['default']['USER'], DB['default']['PASSWORD'], DROP_USER, DROP_DB)

    os.system(SQL)

def run():
    OW_VHOST    = settings.OW_VHOST    
    OW_SITES    = settings.OW_SITES    
    OW_APACHE   = settings.OW_APACHE   

    #exists = list(set(os.listdir(OW_SITES)) | set(os.listdir(OW_VHOST)))
    exists = list(set(os.listdir(OW_SITES)))
    sites = Site.objects.all()
    restart = False

    for site in sites.filter(status=Site.QUEUE):
        #TODO: Check expired site
        if site.name in exists:
            delete(site.name)
        create(site)
        restart = True
        
    delete_sites = list(set(exists) - set([site.name for site in sites]))
    for site_name in delete_sites:
        delete(site_name)
        restart = True

    if restart:
        # enable_virtual_host
        os.system('sudo %s graceful' % OW_APACHE)
        for site in sites.filter(percent__lt=100):
            site.percent = 100
            site.save()

        # Just loop forever
        try:
            while 1: time.sleep(60)
        except KeyboardInterrupt:
            print "Exiting"

# Excute ===================
# run()
if __name__ == '__main__':
    for each in sys.argv[1:]:
        if each == 'run':
            run()
