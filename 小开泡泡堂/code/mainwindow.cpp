#include "mainwindow.h"
#include "ui_mainwindow.h"
#include<qdebug.h>
#include<QDir>
MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    setAttribute(Qt::WA_QuitOnClose);//保证关闭窗口程序能够正常退出
    this->ptimer=new QTimer;//初始化定时器
    this->ui->setupUi(this);
    this->sc=new myscene;//初始化场景
    this->ui->graphicsView->setScene(sc);
    this->toolplayer=new QMediaPlayer;
    setFocusPolicy(Qt::StrongFocus);//聚焦，在让空格键和上下左右键生效的时候用
    connect(toolplayer, SIGNAL(positionChanged(qint64)), this, SLOT(positionChanged(qint64)));
}

//以下板块是音乐添加的函数
void MainWindow::PickProps(){
    QMediaPlayer*p1=new QMediaPlayer;
    p1->setMedia(QUrl::fromLocalFile((QDir::currentPath()+"/music/pickprop.mp3")));
    p1->setVolume(48);p1->play();
}
void MainWindow::bombvoice(){
    QMediaPlayer*p1=new QMediaPlayer;
    p1->setMedia(QUrl::fromLocalFile(QDir::currentPath()+"/music/bombvoice.mp3"));
    p1->setVolume(48);p1->play();
}
void MainWindow::addbloodvoice(){
    QMediaPlayer*p1=new QMediaPlayer;
    p1->setMedia(QUrl::fromLocalFile(QDir::currentPath()+"/music/addbloodvoice.mp3"));
    p1->setVolume(48);p1->play();
}
void MainWindow::firstblood(){
    QMediaPlayer*p1=new QMediaPlayer;
    p1->setMedia(QUrl::fromLocalFile(QDir::currentPath()+"/music/firstblood.mp3"));
    p1->setVolume(48);p1->play();
}
void MainWindow::doublekill(){
    QMediaPlayer*p1=new QMediaPlayer;
    p1->setMedia(QUrl::fromLocalFile(QDir::currentPath()+"/music/double.mp3"));
    p1->setVolume(48);p1->play();
}
void MainWindow::triplekill(){
    QMediaPlayer*p1=new QMediaPlayer;
    p1->setMedia(QUrl::fromLocalFile(QDir::currentPath()+"/music/triple.mp3"));
    p1->setVolume(48);p1->play();
}
void MainWindow::fourkill(){
    QMediaPlayer*p1=new QMediaPlayer;
    p1->setMedia(QUrl::fromLocalFile(QDir::currentPath()+"/music/four.mp3"));
    p1->setVolume(48);p1->play();
}
void MainWindow::fivekill(){
    QMediaPlayer*p1=new QMediaPlayer;
    p1->setMedia(QUrl::fromLocalFile(QDir::currentPath()+"/music/five.mp3"));
    p1->setVolume(48);p1->play();
}
void MainWindow::monsterdie(){
    QMediaPlayer*p1=new QMediaPlayer;
    p1->setMedia(QUrl::fromLocalFile(QDir::currentPath()+"/music/monsterdie.mp3"));
    p1->setVolume(48);p1->play();
}
void MainWindow::getscore(){
    QMediaPlayer*p1=new QMediaPlayer;
    p1->setMedia(QUrl::fromLocalFile(QDir::currentPath()+"/music/getscore.mp3"));
    p1->setVolume(48);p1->play();
}
void MainWindow::countdown(){
    QMediaPlayer*p1=new QMediaPlayer;
    p1->setMedia(QUrl::fromLocalFile(QDir::currentPath()+"/music/countdown.mp3"));
    p1->setVolume(48);p1->play();
}
void MainWindow::speedup(){
    QMediaPlayer*p1=new QMediaPlayer;
    p1->setMedia(QUrl::fromLocalFile(QDir::currentPath()+"/music/02.mp3"));
    p1->setVolume(48);p1->play();
}
void MainWindow::hurt(){
    QMediaPlayer*p1=new QMediaPlayer;
    p1->setMedia(QUrl::fromLocalFile(QDir::currentPath()+"/music/hurt.mp3"));
    p1->setVolume(48);p1->play();
}

//对是否捡到道具的测试，判断依据是人的坐标和道具的坐标是否相等，在每次人物移动时进行触发
void MainWindow::PropsTest(person &p){
    if(sc->item[p.x][p.y]->props==true){
        //然后对道具的名称进行判断不同名称
        PickProps();
        getscore();
      if(sc->item[p.x][p.y]->propssname=="shield"){p.HP++;p.Integral+=10;PropertyShow();sc->item[p.x][p.y]->props=false;}//捡道具给予加分减分setmusic(1,p.propsmusic);//引入音乐}
     else if(sc->item[p.x][p.y]->propssname=="shoes"){p.Speed--;p.Integral+=10;PropertyShow();sc->item[p.x][p.y]->props=false;}
     else if(sc->item[p.x][p.y]->propssname=="snow"){p.Speed+=1;p.Integral-=10;PropertyShow();sc->item[p.x][p.y]->props=false;}
     else if(sc->item[p.x][p.y]->propssname=="addTNT"){p.Explosive_Range++;p.Integral+=10;PropertyShow();sc->item[p.x][p.y]->props=false;}
     else if(sc->item[p.x][p.y]->propssname=="addblood"){p.HP++;p.Integral+=10;PropertyShow();sc->item[p.x][p.y]->props=false;addbloodvoice();}
     //炸弹范围 else if(sc->item[p.x][p.y]->propssname=="addblood"){p.HP++;p.Integral+=10;PropertyShow();sc->item[p.x][p.y]->props=false;}
    }
}

//自定义的功能辅助函数
int max(int a,int b){return a>b?a:b;}
int min(int a,int b){return a<b?a:b;}
//析构函数暂时没用到
MainWindow::~MainWindow()
{
    mon1.HP=mon2.HP=0;
    delete ui;

}
myscene *MainWindow::getScene(){//用于给别的窗口绑定我们的sc层次
    return this->sc;
}

void MainWindow::Monstermove(person&m1,person&m2){//这是两个怪物的智能移动函数，正在尝试用多线程
    while(1&&start==true){
        srand((unsigned)time(nullptr));
        if(m1.HP>0){
        Monsterjudge(m1);
        if(m1.HP==0){sc->item[m1.x][m1.y]->grassappear();m1.x=m1.y=100;}//*在第一个分号前掉落道具，暂时用草代替
        }
        if(m2.HP>0){
        Monsterjudge(m2);
        if(m2.HP==0){sc->item[m2.x][m2.y]->grassappear();m2.x=m2.y=100;}
        }
        if(m1.HP<=0&&m2.HP<=0){break;}
    }
}
void MainWindow::Monsterjudge(person &m){ //在怪兽移动函数中对怪兽是否有移动资格的检测
    int ran=rand()%5;
    if(ran==0){Delay_MSec(250);}
    else if(ran==1){
        Delay_MSec(250);monsterup(m);MeetPerson(m);
    }
    else if(ran==2){
        Delay_MSec(250);monsterdown(m);MeetPerson(m);
    }
    else if(ran==3){
        Delay_MSec(250);monsterleft(m);MeetPerson(m);
    }
    else if(ran==4){
        Delay_MSec(250);monsterright(m);MeetPerson(m);
    }
}

void MainWindow::PropertyShow(){//人物显示在比赛台面上的属性
    ui->label_2->setText("HP is "+QString::number(p1.HP));
    ui->label_3->setText("Integral is "+QString::number(p1.Integral));
    ui->label_5->setText("HP is "+QString::number(p2.HP));
    ui->label_6->setText("Integral is "+QString::number(p2.Integral));
}
void MainWindow::mdisplay(int i, int j,person&mon1){ //怪物的移动显示函数（原理同人类）
    sc->item[i][j]->setmyitem("grass");
    if(sc->item[i][j]->props==true){sc->item[i][j]->setmyitem(sc->item[i][j]->propssname);}
    if(i==mon1.x&&j==mon1.y){sc->item[i][j]->monsterappear();}
}
//怪物的上下左右移动函数
void MainWindow::monsterup(person&m){
    if(Canup(m)){
     qDebug()<<"up";
     m.Direction="up";
     mdisplay(m.x,--m.y,m);mdisplay(m.x,m.y+1,m);
     }
    else{
        monsterright(m);
    }
}
void MainWindow::monsterdown(person&m){
    if(Candown(m)){
    qDebug()<<"down";
    m.Direction="down";
    mdisplay(m.x,++m.y,m);mdisplay(m.x,m.y-1,m);
    }
    else{
        monsterleft(m);
    }
}
void MainWindow::monsterleft(person&m){
    if(Canleft(m)){
    qDebug()<<"left";
    m.Direction="left";
    mdisplay(--m.x,m.y,m);mdisplay(m.x+1,m.y,m);
    }
    else{
        monsterup(m);
    }
}
void MainWindow::monsterright(person&m){
    if(Canright(m)){
    qDebug()<<"right";
    m.Direction="right";
    mdisplay(++m.x,m.y,m);mdisplay(m.x-1,m.y,m);
    }
    else{
        monsterdown(m);
    }
}
//判断是否能上下左右移动
bool MainWindow::Canleft(person&m){
    return !(m.x==0||sc->iswall(m.x-1,m.y)||sc->isbomb(m.x-1,m.y));
}
bool MainWindow::Canright(person&m){
    return !(m.x==19||sc->iswall(m.x+1,m.y)||sc->isbomb(m.x+1,m.y));
}
bool MainWindow::Canup(person&m){
    return !(m.y==0||sc->iswall(m.x,m.y-1)||sc->isbomb(m.x,m.y-1));
}
bool MainWindow::Candown(person&m){
return !(m.y==19||sc->iswall(m.x,m.y+1)==true||sc->isbomb(m.x,m.y+1)==true);
}
//判断怪兽是否碰到人以及人是否碰到怪兽
void MainWindow::MeetPerson(person&m){
    if(p1.x==m.x&&p1.y==m.y){
        p1.HP--;hurt();
        ui->label_2->setText("HP is "+QString::number(p1.HP));
        if(p1.isGG()){start=false;TriggerEndView();}//这里到时要和终止游戏链接起来
        else{qDebug()<<"p1 blood";}//无敌效果暂时不写
        PropertyShow();
    }
    else if(p2.x==m.x&&p2.y==m.y){
        p2.HP--;hurt();
        ui->label_5->setText("HP is "+QString::number(p2.HP));
        if(p2.isGG()){start=false;TriggerEndView();}//这里到时要和终止游戏链接起来
        else{qDebug()<<"p2 blood";}//无敌效果暂时不写
        PropertyShow();
    }

}
void MainWindow::MeetMonster(person&p){//这里有个bug就是这个不会动的怪兽被人碰了之后就不会现形了
    if((p.x==mon1.x&&p.y==mon1.y)||(p.x==mon2.x&&p.y==mon2.y)){
        p.HP--;hurt();
        if(p.isGG()){start=false;TriggerEndView();}//这里到时要和终止游戏链接起来
        else{qDebug()<<"sb blood";}//无敌效果暂时不写
        PropertyShow();
    }
}

//重写键盘响应函数，完成人的上下左右以及放炸弹的操作
void MainWindow::keyPressEvent(QKeyEvent *e)
{
    {
        int time;
        if(p1.Speed>5)time=300*p1.Speed-1200;//这是慢速时，到时还要设计慢速时的持续时间
        else if(p1.Speed<=5)time=100*p1.Speed- 200;
        qDebug()<<p1.Speed<<time;
        _sleep(time);
    }
      if(start==true){
            switch (e->key()) {
            case Qt::Key_W:
               personup();
               MeetMonster(p1);
               PropsTest(p1);
                break;
            case Qt::Key_D:
                personright();
                 MeetMonster(p1);
                 PropsTest(p1);
                break;
            case Qt::Key_S:
                persondown();
                 MeetMonster(p1);
                 PropsTest(p1);
                break;
            case Qt::Key_A:
               personleft();
                 MeetMonster(p1);
                 PropsTest(p1);
                break;
            case Qt::Key_Shift:
               laybomb(p1.x,p1.y,p1);
                break;
            case Qt::Key_I:
               personup2();
                MeetMonster(p2);
                PropsTest(p2);
                break;
            case Qt::Key_L:
                personright2();
                MeetMonster(p2);
                PropsTest(p2);
                break;
            case Qt::Key_K:
                persondown2();
                MeetMonster(p2);
                PropsTest(p2);
                break;
            case Qt::Key_J:
               personleft2();
                MeetMonster(p2);
                PropsTest(p2);
                break;
             case Qt::Key_Slash:
               laybomb(p2.x,p2.y,p2);
               qDebug()<<"enter enter";
                break;
            default:
                break;
            }
    }
}
//对关闭窗口函数进行重写，想办法暂停循环以及结束程序
void MainWindow::closeEvent(QCloseEvent *event){

   toolplayer->stop();start=false;
    this->setAttribute(Qt::WA_DeleteOnClose,true);
    switch( QMessageBox::information( this, tr("exit tip"), tr("Do you really want exit?"), tr("Yes"), tr("No"), 0, 1 ) )
       {
         case 0:
              event->accept();
              break;
         case 1:
         default:
             event->ignore();
             break;
       }
}


//两个人的移动函数以及放置炸弹操作的具体实现
void MainWindow::personup(){
    qDebug()<<"up";
    p1.Direction="up";
      if(p1.y==0||sc->iswall(p1.x,p1.y-1)||sc->isbomb(p1.x,p1.y-1))display(p1.x,p1.y);
       else {display(p1.x,--p1.y);display(p1.x,p1.y+1);}
}
void MainWindow::persondown(){
    qDebug()<<"down";
    p1.Direction="down";
      if(p1.y==19||sc->iswall(p1.x,p1.y+1)==true||sc->isbomb(p1.x,p1.y+1)==true)display(p1.x,p1.y);
       else {display(p1.x,++p1.y);display(p1.x,p1.y-1);}     
}
void MainWindow::personleft(){
    qDebug()<<"left";
    p1.Direction="left";
      if(p1.x==0||sc->iswall(p1.x-1,p1.y)||sc->isbomb(p1.x-1,p1.y))display(p1.x,p1.y);
       else {display(--p1.x,p1.y);display(p1.x+1,p1.y);}

}
void MainWindow::personright(){
    qDebug()<<"right";
    p1.Direction="right";
      if(p1.x==19||sc->iswall(p1.x+1,p1.y)||sc->isbomb(p1.x+1,p1.y))display(p1.x,p1.y);
       else {display(++p1.x,p1.y);display(p1.x-1,p1.y);}
}

void MainWindow::personup2(){
    qDebug()<<"up";
    p2.Direction="up";
      if(p2.y==0||sc->iswall(p2.x,p2.y-1)||sc->isbomb(p2.x,p2.y-1))display(p2.x,p2.y);
       else {display(p2.x,--p2.y);display(p2.x,p2.y+1);}
}
void MainWindow::persondown2(){
    qDebug()<<"down";
    p2.Direction="down";
      if(p2.y==19||sc->iswall(p2.x,p2.y+1)==true||sc->isbomb(p2.x,p2.y+1)==true)display(p2.x,p2.y);
       else {display(p2.x,++p2.y);display(p2.x,p2.y-1);}
}
void MainWindow::personleft2(){
    qDebug()<<"left";
    p2.Direction="left";
      if(p2.x==0||sc->iswall(p2.x-1,p2.y)||sc->isbomb(p2.x-1,p2.y))display(p2.x,p2.y);
       else {display(--p2.x,p2.y);display(p2.x+1,p2.y);}

}
void MainWindow::personright2(){
    qDebug()<<"right";
    p2.Direction="right";
      if(p2.x==19||sc->iswall(p2.x+1,p2.y)||sc->isbomb(p2.x+1,p2.y))display(p2.x,p2.y);
       else {display(++p2.x,p2.y);display(p2.x-1,p2.y);}
}

void MainWindow::laybomb(int x,int y,person&p1){
    int i=0;
    for (;i<p1.BombCapcity;i++){
        if(p1.mybomb[i].isset==true)continue;
        else{p1.mybomb[i].SetLocation_X=x;p1.mybomb[i].SetLocation_Y=y;p1.mybomb[i].isset=true;break;}
    }
    if(i==p1.BombCapcity)return;
    this->sc->item[x][y]->setmyitem("bomb");
    //Delay_MSec是人为定义的延迟函数直接延迟主线程
    Delay_MSec(900);//持续1秒后持续火光，由于线程的影响后放的炸弹会比先放的先爆炸（这是个bug）
    aboutInjure(x,y,p1);//直接检测炸弹中心位
    bombvoice();//输出炸弹声音
    ExplosiveView(x,y,p1);//对炸弹的效果显示以及对相关伤害的计算
     Delay_MSec(400);//持续1秒火光消失
     this->sc->item[x][y]->bomb=false;//还原炸弹爆炸后地板的性质
     p1.mybomb[i].isset=false;//还原地板性质
    ExplosiveRestore(x,y,p1);  //对炸弹爆炸后效果复原处理（涉及道具生成）
}
void MainWindow::display(int i, int j){
    sc->item[i][j]->setmyitem("grass");
    if(sc->isbomb(i,j)==true){sc->item[i][j]->setmyitem("bomb");}
    if(sc->item[i][j]->fire==true){sc->item[i][j]->setmyitem("fire");}
    if(sc->item[i][j]->props==true){sc->item[i][j]->setmyitem(sc->item[i][j]->propssname);}//要把一切道具有关都写到setitem里面
    if(sc->item[i][j]->wall==true){sc->item[i][j]->setmyitem("wall");}
    if(i==p1.x&&j==p1.y)sc->item[i][j]->setmyitem(p1.Direction);
    if(i==p2.x&&j==p2.y)sc->item[i][j]->setmyitem(p2.Direction+"2");
    if(sc->item[i][j]->Mati1==true)sc->item[i][j]->mati1();
    else if(sc->item[i][j]->Mati2==true)sc->item[i][j]->mati2();
    else if(sc->item[i][j]->Mati3==true)sc->item[i][j]->mati3();
    else if(sc->item[i][j]->Mati4==true)sc->item[i][j]->mati4();
    else if(sc->item[i][j]->Mati5==true)sc->item[i][j]->mati5();
    else if(sc->item[i][j]->Mati6==true)sc->item[i][j]->mati6();
    if(sc->item[i][j]->Enlai1==true)sc->item[i][j]->enlaiappear1();
    else if(sc->item[i][j]->Enlai2==true)sc->item[i][j]->enlaiappear2();
    else if(sc->item[i][j]->Enlai3==true)sc->item[i][j]->enlaiappear3();
    else if(sc->item[i][j]->Enlai4==true)sc->item[i][j]->enlaiappear4();
    else if(sc->item[i][j]->Enlai5==true)sc->item[i][j]->enlaiappear5();
    else if(sc->item[i][j]->Enlai6==true)sc->item[i][j]->enlaiappear6();
    if(sc->item[i][j]->Xinkai==true)sc->item[i][j]->xinkai();
}
//人为定义阻碍时间函数
void MainWindow::Delay_MSec(unsigned int msec)
{
    QEventLoop loop;//定义一个新的事件循环
    QTimer::singleShot(msec, &loop, SLOT(quit()));//创建单次定时器，槽函数为事件循环的退出函数
    loop.exec();//事件循环开始执行，程序会卡在这里，直到定时时间到，本循环被退出
}
//爆炸显示函数以及人物怪兽受伤和墙的处理
void MainWindow::ExplosiveView(int x, int y,person&p1){
    //由于有墙的阻碍作用，因此要让函数从炸弹爆炸中心向四周传递以便于判断（详细说明第一种情况，后三种情形同理）
    for(int i=x;i<=19&&i<=x+p1.Explosive_Range;i++){//对炸弹爆炸范围进行限制，不能查过边界并且受人持有的炸弹爆炸范围性质约束
        if(sc->iswall(i,y)==true){//此时设置墙对炸弹的阻碍作用，墙会影响炸弹爆炸效果的延续
            if(sc->isdestroy(i,y)==true){sc->item[i][y]->wall=false;}//如果可摧毁炸弹到了就变成草并且不往下蔓延，如果不可摧毁直接停止炸弹蔓延即可
            display(i,y);//炸弹爆炸效果显示
            break;
        }
        else {sc->item[i][y]->fire=true;sc->item[i][y]->setmyitem("fire");}//对图元相关性质进行设置便于display的显示
    }
    for(int i=x;i>=0&&i>=x-p1.Explosive_Range;i--){
        if(sc->iswall(i,y)==true){
            if(sc->isdestroy(i,y)==true){sc->item[i][y]->wall=false;}//如果可摧毁炸弹到了就变成草并且不往下蔓延，如果不可摧毁直接停止炸弹蔓延即可
            display(i,y);
            break;
        }
        else {sc->item[i][y]->fire=true;sc->item[i][y]->setmyitem("fire");}
    }
    for(int i=y;i<=19&&i<=y+p1.Explosive_Range;i++){
        if(sc->iswall(x,i)==true){
            if(sc->isdestroy(x,i)==true){sc->item[x][i]->wall=false;}//如果可摧毁炸弹到了就变成草并且不往下蔓延，如果不可摧毁直接停止炸弹蔓延即可
            display(x,i);
            break;
        }
        else {sc->item[x][i]->fire=true;sc->item[x][i]->setmyitem("fire");}
    }
    for(int i=y;i>=0&&i>=y-p1.Explosive_Range;i--){
        if(sc->iswall(x,i)==true){
            if(sc->isdestroy(x,i)==true){sc->item[x][i]->wall=false;}//如果可摧毁炸弹到了就变成草并且不往下蔓延，如果不可摧毁直接停止炸弹蔓延即可
            display(x,i);
            break;
        }
        else {sc->item[x][i]->fire=true;sc->item[x][i]->setmyitem("fire");}
    }
}
//爆炸之后的场景复原以及道具生成
void MainWindow::ExplosiveRestore(int x, int y,person&p1){
    //在laybomb函数处理后对炸弹覆盖后的区域进行复原显示
    for(int i=x;i<=min(x+p1.Explosive_Range,19)&&sc->iswall(i,y)==false;i++){sc->item[i][y]->fire=false;this->display(i,y);}
    for(int i=x;i>=max(x-p1.Explosive_Range,0)&&sc->iswall(i,y)==false;i--){sc->item[i][y]->fire=false;this->display(i,y);}
    for(int i=y;i<=min(y+p1.Explosive_Range,19)&&sc->iswall(x,i)==false;i++){sc->item[x][i]->fire=false;this->display(x,i);}
    for(int i=y;i>=max(y-p1.Explosive_Range,0)&&sc->iswall(x,i)==false;i--){sc->item[x][i]->fire=false;this->display(x,i);}
}
//用于人物更新状态
void MainWindow::aboutInjure(int x1, int y1,person&p){//传入爆炸的中心点//其实这里有个bug就是隔墙可以被炸到但是不会显示火光，有时间再改
    if(p1.invincible==false){//这里判断是否无敌状态，无敌状态不受伤害
        //引入cou1，和每个perosn的cou实现英雄联盟的击杀记录机制（可实现firstblood，doublekill（不被连杀中断的情况下））
        if((p1.x==x1&&p1.y<=y1+p.Explosive_Range&&p1.y>=y1-p.Explosive_Range)||(p1.y==y1&&p1.x<=x1+p.Explosive_Range&&p1.x>=x1-p.Explosive_Range)){
            p1.HP--;//在炸弹爆炸范围内则人物会掉血，非己方击杀则对方得到加分，己方HP减少1
            if(p.num==2){p1.cou=0;p2.cou++;p2.Integral+=80;cou1++;}//这里有个bug就是firstblood会重复出现
            if(cou1==1){firstblood();cou1++;}
            if(p2.cou==2)doublekill();
            else if(p2.cou==3)triplekill();
            else if(p2.cou==4)fourkill();
            else if(p2.cou==5)fivekill();
            if(p1.isGG()){start=false;TriggerEndView();}//这里运用一个人物是否死亡函数，以及死亡后触发EndShow窗口出现的函数
            else{qDebug()<<"p1 blood";}//uninjurable(x1,y1)暂时取消人物特效（尝试过多线程但是基础不牢容易出错）：闪动效果,而且执行特效的三秒人物无敌状态（锁定HP），设计在这段时间内执行这两个效果的同时执行其他函数
            PropertyShow();//屏幕上相关属性要在每次结算后进行刷新
        }
    }//p2与p1同理，不展开介绍
    if(p2.invincible==false){
        if((p2.x==x1&&p2.y<=y1+p.Explosive_Range&&p2.y>=y1-p.Explosive_Range)||(p2.y==y1&&p2.x<=x1+p.Explosive_Range&&p2.x>=x1-p.Explosive_Range)){
            p2.HP--;
            if(p.num==1){p2.cou=0;p1.cou++;p1.Integral+=80;cou1++;}
            if(cou1==1){firstblood();cou1++;}
            if(p1.cou==2)doublekill();
            else if(p1.cou==3)triplekill();
            else if(p1.cou==4)fourkill();
            else if(p1.cou==5)fivekill();
            if(p2.isGG()){start=false;TriggerEndView();}//这里到时要和终止游戏链接起来
            else{qDebug()<<"p2 blood";}//uninjurable(x1,y1)暂时取消人物特效（尝试过多线程但是基础不牢容易出错）：闪动效果,而且执行特效的三秒人物无敌状态（锁定HP），设计在这段时间内执行这两个效果的同时执行其他函数
            PropertyShow();
        }
    }
    if((mon1.x==x1&&mon1.y<=y1+p.Explosive_Range&&mon1.y>=y1-p.Explosive_Range)||(mon1.y==y1&&mon1.x<=x1+p.Explosive_Range&&mon1.x>=x1-p.Explosive_Range)){
       mon1.HP--;//怪兽血量减少同人类一致
       sc->item[mon1.x][mon1.y]->props=true;//死亡后掉落道具利用display显示
       sc->item[mon1.x][mon1.y]->propssname="addblood";
        p.Integral+=30;//炸死怪物加炸弹释放者得到加分
        getscore();monsterdie();//音效添加
        PropertyShow();//属性刷新设置
    }
    //mon2与mon1一致，不展开说明
    if((mon2.x==x1&&mon2.y<=y1+p.Explosive_Range&&mon2.y>=y1-p.Explosive_Range)||(mon2.y==y1&&mon2.x<=x1+p.Explosive_Range&&mon2.x>=x1-p.Explosive_Range)){
       mon2.HP--;
       sc->item[mon2.x][mon2.y]->props=true;
       sc->item[mon2.x][mon2.y]->propssname="shoes";
        p.Integral+=50;//炸死怪物加十分
        getscore();monsterdie();
        PropertyShow();
    }
}
//一开始设定作为人物的无敌状态，但是线程这方面知识不太熟练
void MainWindow::uninjurable(int i,int j,person&p1){  //穿入爆炸中心的位置,这个是无敌时间，为他开个线程
    QTime basetime=QTime::currentTime();
    p1.invincible=true;
    while(1){
        sc->item[p1.x][p1.y]->setmyitem("white");
        Delay_MSec(100);
        sc->item[p1.x][p1.y]->setmyitem(p1.Direction);
        Delay_MSec(90);
        if(basetime.msecsTo(QTime::currentTime())>=14000){break;}//此处出现小小的显示bug但是锁血目的已经达到（就这样吧
    }
     p1.invincible=false;
}

//三个按钮的操作，严格按照一般游戏的设置规则
void MainWindow::on_btn_pause_clicked()
{
    if(ui->btn_pause->text()=="Pause"){
        start=false;
        toolplayer->pause();
        ui->btn_pause->setText("Continue");
        ui->btn_stop->setEnabled(false);
    }
    else{
        ui->btn_pause->setText("Pause");
        toolplayer->play();
        connect(this,SIGNAL(toStart()),this,SLOT(ReleaseSuspend()));
         ui->btn_stop->setEnabled(true);
        emit toStart();  
    }
}
void MainWindow::ReleaseSuspend(){  //作为槽函数使用，虽然并没有什么存在的必要
    start=true;
    Monstermove(mon1,mon2);
}
void MainWindow::on_btn_stop_clicked()
{
    if(ui->btn_stop->text()=="Stop"){
        toolplayer->pause();
        start=false;
        ui->btn_stop->setText("ReStart");
        ui->btn_pause->setEnabled(false);
    }
    else{
        ui->btn_stop->setText("Stop");
        ui->btn_start->setEnabled(true);
         ui->btn_stop->setEnabled(false);
          ui->btn_pause->setEnabled(false);
         if(MapChoose ==0)getScene()->map1();
         else if(MapChoose ==1)getScene()->map2();
         else if(MapChoose ==2)getScene()->map3();
         StartPerson();
    }
    mon1.HP=mon2.HP=0;
}
void MainWindow::on_btn_start_clicked()
{
    countdown();
    ui->label->setText("Moon");
    ui->label_4->setText("Sun");
    PropertyShow();
    StartPerson();
    ui->btn_start->setEnabled(false);
    toolplayer->setMedia(QUrl::fromLocalFile(QDir::currentPath()+"/music/01.mp3"));
    toolplayer->setVolume(15);
        Delay_MSec(3000);
        start=true;
        *basetime=QTime::currentTime();
    toolplayer->play();
    ui->btn_pause->setEnabled(true);
    ui->btn_stop->setEnabled(true);
    Monstermove(mon1,mon2);
 }
//对人物初始化和场景初始化的设置
void MainWindow::StartPerson(){
    p1.num=1;p2.num=2;
    if(MapChoose==0){
        p1.setperson(2,2);this->sc->setpic(p1.x,p1.y,"person");
        p2.setperson(18,18);this->sc->item[18][18]->personappear2();
        mon2.monster=mon1.monster=true;
        mon1.setmonster(5,5);this->sc->item[5][5]->monsterappear();
        mon2.setmonster(11,6);this->sc->item[11][6]->monsterappear();
    }
    else if(MapChoose==2){
        p1.setperson(2,2);this->sc->setpic(p1.x,p1.y,"person");
        p2.setperson(15,15);this->sc->item[15][15]->personappear2();
        mon2.monster=mon1.monster=true;
        mon1.setmonster(10,3);this->sc->item[10][3]->monsterappear();
        mon2.setmonster(10,18);this->sc->item[10][18]->monsterappear();
    }
    else if(MapChoose==1){
        p1.setperson(0,0);this->sc->setpic(p1.x,p1.y,"person");
        p2.setperson(19,19);this->sc->item[19][19]->personappear2();
        mon2.monster=mon1.monster=true;
        mon1.setmonster(0,19);this->sc->item[0][19]->monsterappear();
        mon2.setmonster(19,0);this->sc->item[19][0]->monsterappear();
    }
    //人物和怪兽出现要人为设定
}
//在判定人物死亡之后弹出结束窗口的响应函数
void MainWindow::TriggerEndView(){
    if(p1.HP==0){end->winP=&p2;end->loseP=&p1;}
    else if(p2.HP==0){end->winP=&p1;end->loseP=&p2;}
    end->TimeText=Timeup();
    end->sumTime=sumtime;
    toolplayer->stop();
    InputBox=new Enter_Information;
    InputBox->exec();
    end->otherOperation();
    end->exec();
    if(end->gameover==true)this->close();
    ui->btn_pause->setEnabled(false);
    ui->btn_stop->setText("ReStart");
    ui->btn_start->setEnabled(false);
}
//记录时间的函数
QString MainWindow::Timeup(){
    QTime current=QTime::currentTime();
    sumtime=basetime->msecsTo(current);
    QTime showtime(0,0,0,0);
    showtime=showtime.addMSecs(sumtime);
    timerecord=showtime.toString("hh:mm:ss:zzz");
    return timerecord;
}

