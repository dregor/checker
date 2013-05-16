#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, argparse, pickle, io
from check import Site

curdir =  os.path.dirname(os.path.abspath(__file__)) 
image_dir = os.path.join(curdir,'images')

def save(site):
    result = ''
    try:
        image = io.open( os.path.join(image_dir,(site.name+'.pp')),'wb')
    except:
        result = 'Write to file error!' + str(sys.exc_info())
    else:
        pickle.dump( site, image )
        result = 'Write to - ' + site.name +'.pp'
        image.close()
    finally:
        return result
    
def read( name ):
        file = io.open( os.path.join(image_dir,name),'rb')
        site = pickle.load( file )
        print( 'Load from : ' + str(file) + '\n' + str(site))
        file.close()
        return site
    
def read_all( path = None ):
    if (path == None):
        path = image_dir
    for ( root, dirs, files ) in os.walk(path):
        for name in files:
            fullname = os.path.join( root, name )
            if (fullname[-3:]=='.pp'):
                file = io.open( fullname, 'rb' )
                check( name )

def check( name ):
    site = read( name )
    print('Site - %s, Matches - %f, deviation - %f' % (site.name, site.compare(), site.deviation ))
    
    
def main():
    if not os.path.isdir( image_dir ):
        os.mkdir(image_dir)
    
    parser = argparse.ArgumentParser(description='Parse sites.')
    subparsers = parser.add_subparsers(help='Variants job:', dest='vary')
    image_parser = subparsers.add_parser('image', help='Create image site.')
    check_parser = subparsers.add_parser('check',help='Check sites.')
    
    image_parser.add_argument('-u', '--url',
                            default = None,
                            dest = 'url',
                            help ='URL site')
    
    image_parser.add_argument('-n','--name',
                              dest = 'name',
                              default = None,
                              help = 'name image site.')
    
    check_parser.add_argument('-n','--name',
                              dest = 'name',
                              default = None,
                              help = 'name image site.')
    
    pars = parser.parse_args()
    
    if pars.vary == 'image':
        if pars.url != None and pars.name != None:
            site = Site( url = pars.url, name = pars.name )
            print( save(site) ) 
            print('deviation %f .' % site.deviation)
        else:
            print('Enter URL and image name. See -h or --help.')
    else:
        if pars.name == None:
            read_all()
        else:
            check( pars.name + '.pp' )
            
if __name__ == '__main__':
    main()
            