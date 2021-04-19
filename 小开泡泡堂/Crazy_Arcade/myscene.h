#ifndef MYSCENE_H
#define MYSCENE_H

#include <QObject>
#include<QGraphicsScene>
#include<myitem.h>
class myscene : public QGraphicsScene
{
    friend person;
    Q_OBJECT
public:
    explicit myscene(QObject *parent = nullptr);
    explicit myscene(int map);
    void setpic(int i,int j,QString s1);
    myitem*item[20][20];
    bool iswall(int x,int y){return item[x][y]->wall;}//判断是否有阻隔效果
    void setwall(int x,int y){item[x][y]->wall=true;item[x][y]->wallappear(); }
    bool isbomb(int x,int y){return item[x][y]->bomb;}//判断是否有bomb
    void setbomb(int x,int y){item[x][y]->bomb=true;item[x][y]->bombappear(); }
    bool isdestroy(int x,int y){return item[x][y]->destroy;}//能被摧毁返回true
    void setProps();
    int shoes;

    void map1();
    void map2();
    void map3();
signals:

public slots:
};

#endif // MYSCENE_H
