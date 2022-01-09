#include "myitem.h"

myitem::myitem(QString s1)
{

    if(s1=="grass"){grassappear();}
    else if(s1=="person"){personappear();}
    else if(s1=="up"){upappear();}
    else if(s1=="down"){downappear();}
    else if(s1=="left"){leftappear();}
    else if(s1=="right"){rightappear();}
    else if(s1=="up2"){upappear2();}
    else if(s1=="down2"){downappear2();}
    else if(s1=="left2"){leftappear2();}
    else if(s1=="right2"){rightappear2();}
    else if(s1=="bomb"){bombappear();this->bomb=true;}
    else if(s1=="fire"){fireappear();this->fire=true;}
    else if(s1=="invincible"){invincibleappear();}
    else if(s1=="white"){whiteappear();}
    else if(s1=="wall"){wallappear();}
    else if(s1=="monster"){monsterappear();}

}
void myitem::setmyitem(QString s1)
{

    if(s1=="grass"){grassappear();}
    else if(s1=="person"){personappear();}
    else if(s1=="up"){upappear();}
    else if(s1=="down"){downappear();}
    else if(s1=="left"){leftappear();}
    else if(s1=="right"){rightappear();}
    else if(s1=="up2"){upappear2();}
    else if(s1=="down2"){downappear2();}
    else if(s1=="left2"){leftappear2();}
    else if(s1=="right2"){rightappear2();}
    else if(s1=="bomb"){bombappear();bomb=true;}
    else if(s1=="fire"){fireappear();this->fire=true;}
    else if(s1=="invincible"){invincibleappear();}
    else if(s1=="white"){whiteappear();}
    else if(s1=="wall"){wallappear();}
    else if(s1=="monster"){monsterappear();}
    else if(s1=="shield"){shield();}
    else if(s1=="shoes"){shoes();}
    else if(s1=="addTNT"){addTNT();}
    else if(s1=="addblood"){addblood();}
    else if(s1=="snow"){snow();}
}
void myitem::showProps(){
    if(this->propssname=="shield")
        this->shield();
    else if(this->propssname=="shoes")
        this->shoes();
    else if(this->propssname=="addblood")
        this->addblood();
    else if(this->propssname=="addTNT")
        this->addTNT();
    else if(this->propssname=="snow")
        this->snow();
}
void myitem::setPropssname(int pro){
    if(pro>=0&&pro<3)
        this->propssname="shield";
    else if(pro>=3&&pro<6)
        this->propssname="shoes";
    else if(pro>=6&&pro<9)
        this->propssname="addblood";
    else if(pro>=9&&pro<12)
        this->propssname="addTNT";
    else if(pro==12)
        this->propssname="snow";
}

