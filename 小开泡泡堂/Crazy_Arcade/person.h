#ifndef PERSON_H
#define PERSON_H
#include<QMediaPlayer>
#include <QObject>
#include<QDebug>
#include<QTime>
#include<QTimer>
#include"bomb.h"
//#include<mainwindow.h>
class MainWindow;

class person : public QObject
{
    Q_OBJECT

public:
    person(QObject *parent = nullptr);
    void setperson(int x,int y,int speed=3);
    int num=0;//区别是p1还是p2
    int BombCapcity=1;
    int Speed;//走一步需要的时间  正常延迟0.3s执行代码 加速一次就是减0.1s,减速就是加0.3s
    int HP;
    int Explosive_Range;
    QString Direction; //直接字符串表示上下左右
    int x;
    int y;//坐标
    int Integral=0;//积分，敌方死亡+10
    bool monster=false; //是否是怪物
    bool invincible; //是否无敌状态
    bomb mybomb[5];
    QMediaPlayer* propsmusic;

    int cou=0;//记录杀敌

    void setBombCapcity(int t){BombCapcity=t;}
    void setSpeed(int s){Speed=s;}
    void setHp(int h){HP=h;}
    void setExplosiveRange(int er){Explosive_Range=er;}
    void setDirection(QString s){Direction=s;}
    void setLocation(int x,int y){this->x=x;this->y=y;}
    bool isGG(){if(HP>0)return false;else return true;} //在每次收到伤害时触发，返回true则代表gg，然后发出GameOver
    void setmonster(int x,int y);
    person&operator=(person& p1);
signals:

public slots:
};



#endif // PERSON_H
