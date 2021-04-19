#include "endshow.h"
#include "ui_endshow.h"
#include<QMovie>
#include<QDir>
EndShow::EndShow(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::EndShow)
{
    ui->setupUi(this);
    //this->setAttribute(Qt::WA_DeleteOnClose,true);
    toolplayer=new QMediaPlayer;
    toolplayer2=new QMediaPlayer;
}
void EndShow::otherOperation(){
    gameovervoice();gameovervoice2();
    QString text="";
    integralRecord=winP->Integral;
    if(winP->num==2){text="Moon GG!!!\nMoon Integral:";text+=QString::number(loseP->Integral);text+="\nSun Integral:";text+=QString::number(winP->Integral);text+='\n';}
    else if(winP->num==1){text="Sun GG!!! \nSun Integral:";text+=QString::number(loseP->Integral);text+="\nMoon Integral:";text+=QString::number(winP->Integral);text+='\n';}
     text+="Time Using:";text+=TimeText;
    ui->text->setText(text);//对相关数据的收集与展示
    QMovie* move = new QMovie(QDir::currentPath()+"/pic/gameovervideo.gif");
        ui->moive->setMovie(move);//实现音频文件引入
        if(PauseSave::name.length()!=0&&PauseSave::id.length()!=0){//对是否写入内容进行判断
            QString cnt="";
           cnt+=PauseSave::name;cnt+=" ";cnt+=PauseSave::id;cnt+=" ";cnt+=QString::number(integralRecord);cnt+=" ";cnt+=TimeText;cnt+='\n';
            writetoFile(cnt);
        }
        move->start();
}
void EndShow::gameovervoice(){
    toolplayer->setMedia(QUrl::fromLocalFile(QDir::currentPath()+"/music/03.mp3"));
    toolplayer->setVolume(24);toolplayer->play();
}
void EndShow::gameovervoice2(){
    toolplayer2->setMedia(QUrl::fromLocalFile(QDir::currentPath()+"/music/04.mp3"));
    toolplayer2->setVolume(24);toolplayer2->play();
}

void EndShow::writetoFile(QString cnt){
    QFile file("RankData.txt");
    if(!file.open(QIODevice::Append|QIODevice::Text)){QMessageBox::critical(this,"error","file open abnormal,nothing save","comfirm");return;}
    QTextStream out(&file);
    out<<cnt;
    file.close();
}
EndShow::~EndShow()
{
    delete ui;
}
void EndShow::closeEvent(QCloseEvent *event){
    toolplayer->stop();toolplayer2->stop();
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
void EndShow::on_pushButton_clicked()//游戏结束，直接结束进程
{
    toolplayer->stop();toolplayer2->stop();
    gameover=true;
    this->close();
}
void EndShow::on_pushButton_3_clicked()//游戏排行榜出现
{
    toolplayer->stop();toolplayer2->stop();
    Ranking*r=new Ranking;
    r->heroeslist();
    r->exec();
}
