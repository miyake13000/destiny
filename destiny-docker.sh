#!/bin/bash

#This script only works under below conditions
# 1. Docker is installed

function usage(){
    cat <<_EOT_
destiny-docker.sh

Usage:
    $0 Option

Description:
    start and stop destiny on container

Options:
    start      start destiny on container
    stop       stop destiny
    status     show destiny's condition
    restart    stop and restart container
    update     update container image
    help       show this usage
    [command]  execute [command] in container
_EOT_
}

function main(){
    if ! user_is_member_of_dockergroup; then
        echo "You have to be member of docker group"
        exit 1
    fi

    cd "$(dirname "$0")"

    case "$1" in
        start)
            start
            ;;
        stop)
            stop
            ;;
        status)
            status
            ;;
        restart)
            restart
            ;;
        update)
            update
            ;;
        help)
            usage
            ;;
        "")
            usage >&2
            exit 1
            ;;
        *)
            start_with_command "$1"
            ;;
    esac
    return 0
}

function user_is_member_of_dockergroup(){
    if [ $(groups | grep -c -e docker -e root) = 0 ]; then
        return 1
    fi
    return 0
}

function start(){
    if is_container_running destiny; then
        echo "destiny has already runnning"
    else
        echo -n "try to start destiny..."
        docker run -d --name destiny -p 8080:80 \
            -v $PWD/cgi-bin:/usr/local/apache2/cgi-bin \
            -v $PWD/lib:/usr/local/apache2/lib \
            -v $PWD/db:/usr/local/apache2/db \
            -v $PWD/conf/httpd.conf:/usr/local/apache2/conf/httpd.conf  \
            destiny > /dev/null
        if [ $? = 0 ]; then
            echo "done."
        else
            exit 1
        fi
    fi
}

function start_with_command(){
    if is_container_running destiny; then
        echo "destiny has already runnning"
    else
        docker run -it --name destiny -p 8080:80 \
            -v $PWD/cgi-bin:/usr/local/apache2/cgi-bin \
            -v $PWD/lib:/usr/local/apache2/lib \
            -v $PWD/db:/usr/local/apache2/db \
            destiny $@
    fi
}

function stop(){
    if is_container_running destiny; then
        echo -n "try to stop destiny..."
        docker stop destiny > /dev/null 2>&1
        docker rm destiny > /dev/null
        if [ $? = 0 ]; then
            echo "done."
        else
            exit 1
        fi
    else
        echo "destiny is not running"
    fi
}

function status(){
    if is_container_running destiny; then
        echo "running"
    else
        echo "stop"
    fi
}

function restart(){
    if is_container_running destiny; then
        stop
        start
    else
        echo "destiny is not runnning"
    fi
}

function update(){
    if is_container_running destiny; then
        echo -n "try to update destiny container..."
        docker commit -c 'CMD ["/docker-entrypoint.sh"]' destiny destiny > /dev/null
        echo "done"
    else
        echo "destiny container does not exist"
    fi
}

function is_container_running(){
    res=$(docker ps -a --format "table {{.Names}}" |grep -cx "$1")
    if [ $res = 0 ]; then
        return 1
    else
        return 0
    fi
}

main "$@"
