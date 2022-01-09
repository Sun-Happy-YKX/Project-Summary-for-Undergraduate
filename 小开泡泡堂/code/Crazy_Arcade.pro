#-------------------------------------------------
#
# Project created by QtCreator 2019-07-03T17:52:01
#
#-------------------------------------------------

QT       += core gui
QT       += multimedia

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = Crazy_Arcade
TEMPLATE = app

# The following define makes your compiler emit warnings if you use
# any feature of Qt which has been marked as deprecated (the exact warnings
# depend on your compiler). Please consult the documentation of the
# deprecated API in order to know how to port your code away from it.
DEFINES += QT_DEPRECATED_WARNINGS

# You can also make your code fail to compile if you use deprecated APIs.
# In order to do so, uncomment the following line.
# You can also select to disable deprecated APIs only up to a certain version of Qt.
#DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0x060000    # disables all the APIs deprecated before Qt 6.0.0

CONFIG += c++11

SOURCES += \
        bomb.cpp \
        endshow.cpp \
        enter_information.cpp \
        main.cpp \
        mainwindow.cpp \
        myitem.cpp \
        myscene.cpp \
        pausesave.cpp \
        person.cpp \
        ranking.cpp \
        start.cpp

HEADERS += \
        bomb.h \
        endshow.h \
        enter_information.h \
        mainwindow.h \
        myitem.h \
        myscene.h \
        pausesave.h \
        person.h \
        ranking.h \
        start.h

FORMS += \
        endshow.ui \
        enter_information.ui \
        mainwindow.ui \
        ranking.ui

# Default rules for deployment.
qnx: target.path = /tmp/$${TARGET}/bin
else: unix:!android: target.path = /opt/$${TARGET}/bin
!isEmpty(target.path): INSTALLS += target

RESOURCES += \
    rc.qrc
