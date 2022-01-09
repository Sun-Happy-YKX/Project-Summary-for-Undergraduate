#ifndef MYITEM_H
#define MYITEM_H
#include"person.h"
#include <QObject>
#include<QGraphicsPixmapItem>
#include<qstring.h>
#include<QTime>
class myitem : public QGraphicsPixmapItem
{
    friend person;
public:
    void setmyitem(QString s1);
    myitem(QString s1);
    void personappear(){this->setPixmap(QPixmap(":/bg/pic/person.png"));}
    void grassappear(){this->setPixmap(QPixmap(":/bg/pic/1.png"));}
    void upappear(){this->setPixmap(QPixmap(":/bg/pic/up.png"));}
    void downappear(){this->setPixmap(QPixmap(":/bg/pic/down.png"));}
    void leftappear(){this->setPixmap(QPixmap(":/bg/pic/left.png"));}
    void rightappear(){this->setPixmap(QPixmap(":/bg/pic/right.png"));}

    void personappear2(){this->setPixmap(QPixmap(":/bg/pic/person2.png"));}
    void upappear2(){this->setPixmap(QPixmap(":/bg/pic/sunup.png"));}
    void downappear2(){this->setPixmap(QPixmap(":/bg/pic/sundown.png"));}
    void leftappear2(){this->setPixmap(QPixmap(":/bg/pic/sunleft.png"));}
    void rightappear2(){this->setPixmap(QPixmap(":/bg/pic/sunright.png"));}

    void bombappear(){this->setPixmap(QPixmap(":/bg/pic/bomb.png"));}
    void fireappear(){this->setPixmap(QPixmap(":/bg/pic/fire.png"));}
    void invincibleappear(){this->setPixmap(QPixmap(":/bg/pic/invincible.png"));}
    void whiteappear(){this->setPixmap(QPixmap(":/bg/pic/white.png"));}
    void monsterappear(){this->setPixmap(QPixmap(":/bg/pic/monster.png"));}

     void enlaiappear1(){this->setPixmap(QPixmap(":/bg/pic/enlai1.png"));wall=true;destroy=false;props=false;Enlai1=true; }
     void enlaiappear2(){this->setPixmap(QPixmap(":/bg/pic/enlai2.png"));wall=true;destroy=false;props=false;Enlai2=true;}
     void enlaiappear3(){this->setPixmap(QPixmap(":/bg/pic/enlai3.png"));wall=true;destroy=false;props=false;Enlai3=true;}
     void enlaiappear4(){this->setPixmap(QPixmap(":/bg/pic/enlai4.png"));wall=true;destroy=false;props=false;Enlai4=true;}
     void enlaiappear5(){this->setPixmap(QPixmap(":/bg/pic/enlai5.png"));wall=true;destroy=false;props=false;Enlai5=true;}
     void enlaiappear6(){this->setPixmap(QPixmap(":/bg/pic/enlai6.png"));wall=true;destroy=false;props=false;Enlai6=true;}
     void mati1(){this->setPixmap(QPixmap(":/bg/pic/mati1.png"));wall=true;destroy=false;props=false;Mati1=true; }
     void mati2(){this->setPixmap(QPixmap(":/bg/pic/mati2.png"));wall=true;destroy=false;props=false;Mati2=true;}
     void mati3(){this->setPixmap(QPixmap(":/bg/pic/mati3.png"));wall=true;destroy=false;props=false;Mati3=true;}
     void mati4(){this->setPixmap(QPixmap(":/bg/pic/mati4.png"));wall=true;destroy=false;props=false;Mati4=true;}
     void mati5(){this->setPixmap(QPixmap(":/bg/pic/mati5.png"));wall=true;destroy=false;props=false;Mati5=true;}
     void mati6(){this->setPixmap(QPixmap(":/bg/pic/mati6.png"));wall=true;destroy=false;props=false;Mati6=true;}
     void xinkai(){this->setPixmap(QPixmap(":/bg/pic/xinkai.png"));wall=true;destroy=false;props=false;Xinkai=true;}

     void wallappear(){this->setPixmap(QPixmap(":/bg/pic/wall.png"));wall=true;destroy=false;props=false;}
     void treeappear(){this->setPixmap(QPixmap(":/bg/pic/tree.png"));wall=true;destroy=true;}
     void redtreeappear(){this->setPixmap(QPixmap(":/bg/pic/redtree.png"));wall=true;destroy=true;}


     void shield(){this->setPixmap(QPixmap(":/bg/pic/shield.png"));}
     void shoes(){this->setPixmap(QPixmap(":/bg/pic/shoes.png"));}
     void addblood(){this->setPixmap(QPixmap(":/bg/pic/addblood.png"));}
     void addTNT(){this->setPixmap(QPixmap(":/bg/pic/addTNT.png"));}
     void snow(){this->setPixmap(QPixmap(":/bg/pic/snow.png"));};

     void showProps();
     void setPropssname(int pro);
     void setProp(){this->props=true;}

        bool wall;
        bool destroy=true;//这个要人为初始化，姑且为true
        bool props=false;//这个是在有墙的时候给他出初始化的一个墙的性质
        QString  propssname="";//这里拥有的道具的名字（要靠他进行if判断）

        bool bomb;
        bool fire; //此处用火代指爆炸范围，只要为true就是收到伤害
        bool Xinkai=false;
        bool Enlai1=false;
        bool Enlai2=false;
        bool Enlai3=false;
        bool Enlai4=false;
        bool Enlai5=false;
        bool Enlai6=false;

        bool Mati1=false;
        bool Mati2=false;
        bool Mati3=false;
        bool Mati4=false;
        bool Mati5=false;
        bool Mati6=false;
};

#endif // MYITEM_H
