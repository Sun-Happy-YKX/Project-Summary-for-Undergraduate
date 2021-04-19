#ifndef PAUSESAVE_H
#define PAUSESAVE_H
#include<qstring.h>
#include <QObject>
//这个文件所人都包含，可以用来储存和调用需要使用的变量（一定程度解决两头文件相互包含的问题）
class PauseSave : public QObject
{
    Q_OBJECT
public:
    explicit PauseSave(QObject *parent = nullptr);
     static QString name;
     static QString id;
signals:

public slots:
};

#endif // PAUSESAVE_H
