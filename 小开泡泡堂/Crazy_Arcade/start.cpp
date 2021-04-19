#include "start.h"
#include<QPalette>
#include<QPixmap>
#include<QPainter>
#include<QPaintEvent>
Start::Start(QWidget *parent) : QWidget(parent)
{ 
    this->setAttribute(Qt::WA_DeleteOnClose,true);
    this->w=new MainWindow;
       setWindowFlags(windowFlags()&~Qt::WindowMaximizeButtonHint);    //禁止最大化
       this->setGeometry(600,70,700,800);//以下是相关性质设置
       setFixedSize(this->width(),this->height());      //禁止拖动窗口大小
       this->setAutoFillBackground(true);
       QPalette palette;//插入图片
       QPixmap pixmap(":/bg/pic/nkjinnan.gif");
       palette.setBrush(QPalette::Window, QBrush(pixmap));
       this->setPalette(palette);
       this->label=new QLabel("Please Choose the Map",this);
       this->label->setStyleSheet("font-size:30px");
       this->label->setGeometry(200,100,400,50);
       this->label->show();
       this->button[0]=new QPushButton("Balitai Campus",this);
       this->button[0]->setGeometry(230,250,250,50);
       this->button[0]->setStyleSheet("background-image:url(:/bg/pic/background1.png)");
       this->button[1]=new QPushButton("Jinnan Campus",this);
       this->button[1]->setGeometry(230,400,250,50);
       this->button[1]->setStyleSheet("background-image:url(:/bg/pic/background2.png)");
       this->button[2]=new QPushButton("Taida Campus",this);
       this->button[2]->setGeometry(230,550,250,50);
       this->button[2]->setStyleSheet("background-image:url(:/bg/pic/background3.png)");
       for(int i=0;i<3;i++){
           this->button[i]->show();
       }
    connect(this->button[0], &QPushButton::clicked,
            [=]()
    {
        this->w->getScene()->map1();
        this->w->show();
        this->w->MapChoose=0;
        w->sc->setProps();
        this->hide();
    });
    connect(this->button[1], &QPushButton::clicked,
            [=]()
    {
        this->hide();
        this->w->getScene()->map2();
        this->w->show();
        this->w->MapChoose=1;
        w->sc->setProps();
    });
    connect(this->button[2], &QPushButton::clicked,
            [=]()
    {
        this->hide();
        this->w->getScene()->map3();
        this->w->show();
        this->w->MapChoose=2;
        w->sc->setProps();
    });
}
