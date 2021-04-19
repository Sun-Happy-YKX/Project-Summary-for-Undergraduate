#ifndef MAINWINDOW_H
#define MAINWINDOW_H
#include<QApplication>
#include <QMainWindow>
#include<myscene.h>
#include"person.h"
#include<stdlib.h>
#include<time.h>
#include<qthread.h>
#include<QKeyEvent>
#include<qmessagebox.h>
#include <iostream>
#include<qobject.h>
#include<QTimer>
#include<QTime>
#include<qmutex.h>
#include<qmediaplayer.h>
#include<QMediaPlaylist>
#include<QPaintEvent>
#include<QPainter>
#include"endshow.h"
#include"enter_information.h"
namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT
    friend myitem;friend person;
    friend int max(int,int);
    friend int min(int,int);
public:
    explicit MainWindow(QWidget *parent = nullptr);
    ~MainWindow();
    void keyPressEvent(QKeyEvent *e);
    person p1,p2,tool;//tool是工具人，用来模拟炸弹和人的效果对，所以其要特别的初始化
    person mon1,mon2;
    QTimer*ptimer;
    Enter_Information* InputBox;
    myscene* sc;
    bool start=false;//内部程序是否开始运行
    myscene *getScene();
    int MapChoose=4;
    QTime *basetime=new QTime;

    EndShow* end=new EndShow;
    QMediaPlayer*toolplayer,*Speedup;//这个是总起的背景音乐

    QString Timeup();
    QString timerecord;
    int sumtime=0;

    void PropsTest(person&);//这个检验函数同时也要对人物属性进行处理
    void PickProps();
     void bombvoice();
      void addbloodvoice();
      void firstblood();
      void doublekill();
      void triplekill();
      void fourkill();
      void fivekill();
      void monsterdie();
      void getscore();
      void countdown();
      void speedup();
      void hurt();

    void personup();
    void persondown();
    void personleft();
    void personright();
    void personup2();
    void persondown2();
    void personleft2();
    void personright2();
    void monsterup(person&);
    void monsterdown(person&);
    void monsterleft(person&);
    void monsterright(person&);
    void Monsterjudge(person&);
     bool Canleft(person&);
     bool Canright(person&);
     bool Canup(person&);
     bool Candown(person&);


    void StartPerson();
    void laybomb(int x,int y,person&);
    void ExplosiveView(int x,int y,person&);//同时设置了以此为远点周围的爆炸属性
    void ExplosiveRestore(int x,int y,person&);//同时复原了以此为远点周围的爆炸属性

    void display(int i,int j);
    void mdisplay(int i,int j,person&mon1); //怪物移动
    void Delay_MSec(unsigned int msec);//sleep是阻碍线程的，Delay_MSec是阻碍多线程其中一个线程的

    void closeEvent(QCloseEvent *event);


    int pausex=0;
    int pausey=0;//用于解决槽函数不能传参的问题临时储存
    person*pauseperson;
    bool isfirstblood=false;//true则可以
    int cou1=0;//记录次数
public slots:
    void on_btn_start_clicked();
    void aboutInjure(int x,int y,person&);//爆炸时触发检查人在不在爆炸范围内,无需返回值
    void uninjurable(int i,int j,person&);//掉一滴血时的无敌状态
    void Monstermove(person&,person&);
    void MeetPerson(person&);//传入怪兽
    void MeetMonster(person&);//传入人
    void PropertyShow();

    void TriggerEndView();
signals:
    void toStart();
private slots:
    void on_btn_pause_clicked();
    void on_btn_stop_clicked();
    void ReleaseSuspend();
private:
    Ui::MainWindow *ui;

};

#endif // MAINWINDOW_H
