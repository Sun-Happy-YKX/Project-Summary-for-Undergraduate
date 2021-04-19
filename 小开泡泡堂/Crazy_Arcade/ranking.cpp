#include "ranking.h"
#include "ui_ranking.h"
#include<QFile>
#include<QTextStream>
#include<QMessageBox>
#include<QDebug>
#include<QDir>
#include<QFont>
Ranking::Ranking(QDialog *parent) :
    QDialog(parent),
    ui(new Ui::Ranking)
{
    this->setStyleSheet("background-image:url(:/bg/pic/rank.jpg)");
    toolplayer=new QMediaPlayer;
   // this->setAttribute(Qt::WA_DeleteOnClose,true);
    ui->setupUi(this);
    setHeaderItem();
    int ret=readFile();
    if(!ret){QMessageBox::critical(this,"Error","File open abnormal","Comfirm");this->close();}
    else{
        for(int i=0;i<stu_lines.length();i++)
           qDebug()<<stu_lines.at(i);
        qDebug()<<"finished read"<<endl;
    }
    DoQurry();
}
void Ranking::setHeaderItem(){
    this->model=new QStandardItemModel;//在此要设置表头（Model方法）
    model->setHorizontalHeaderItem(0,new QStandardItem("Name"));
    model->setHorizontalHeaderItem(1,new QStandardItem("ID"));
    model->setHorizontalHeaderItem(2,new QStandardItem("Score"));
    model->setHorizontalHeaderItem(3,new QStandardItem("Use Time"));
    this->ui->tableView->setModel(model);
    ui->tableView->setColumnWidth(0,100);
    ui->tableView->setColumnWidth(1,100);
    ui->tableView->setColumnWidth(2,100);
    ui->tableView->setColumnWidth(3,100);
}
Ranking::~Ranking()
{
    delete ui;
}
void swap(QStringList&a,QStringList&b){QStringList t;t=a;a=b;b=t;}//认为定义容器类交换函数
int Ranking::readFile(){//实现文件读取功能
    QFile file("RankData.txt");
         if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
             return 0;
         QTextStream in(&file);
         while (!in.atEnd()) {
             QString line = in.readLine();
             stu_lines.append(line);
         }
     file.close();
     return 1;   //如果点击搜索之后再读取的话每次搜索都要重新读取一遍，效率极低，我们往往采取将其放入构造函数内一开始就进行读取
}
void  Ranking::DoQurry(){
    int cou=0;QStringList vessel[20];
    for(int i=0;i<stu_lines.length();i++){
        QString line=stu_lines.at(i);
        line= line.trimmed(); //去掉末尾空白
        qDebug()<<line;
        vessel[cou++]=line.split(" ");
    }
    //按分数从大到小排列
    for (int i=0;i<stu_lines.length()-1;i++) {
        //vessel[i].at(2);
        for (int j=i+1;j<stu_lines.length();j++) {
            if(vessel[i].at(2)<vessel[j].at(2))swap(vessel[i],vessel[j]);
       }
    }
    for(int i=0;i<stu_lines.length();i++){if(vessel[i].at(0)=="invalid"||vessel[i].at(1)=="invalid");Display(i,vessel[i]);}
}
void Ranking::Display(int row, QStringList vessel){//传入行数和那行的vessel即可
    for(int i=0;i<4;i++)
        this->model->setItem(row,i,new QStandardItem(vessel.at(i)));
}
void Ranking::heroeslist(){
    toolplayer->setMedia(QUrl::fromLocalFile(QDir::currentPath()+"/music/05.mp3"));
    toolplayer->setVolume(24);toolplayer->play();
}
