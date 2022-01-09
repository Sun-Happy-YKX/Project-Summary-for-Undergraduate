#include "person.h"
#include<QMessageBox>
person::person(QObject *parent) : QObject(parent)
{
    Speed=5;BombCapcity=Explosive_Range=2;HP=2;monster=invincible=false;

}
void person::setperson(int x,int y,int speed){
    this->x=x;this->y=y;this->Speed=speed;BombCapcity=Explosive_Range=2;HP=2;
    monster=invincible=false;
    propsmusic=new QMediaPlayer;
}
void person::setmonster(int x,int y){
    this->x=x;this->y=y;;BombCapcity=Explosive_Range=0;HP=1;
    invincible=false;monster=true;
}

