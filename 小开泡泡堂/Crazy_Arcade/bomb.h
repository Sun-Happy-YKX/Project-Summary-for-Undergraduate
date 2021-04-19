#ifndef BOMB_H
#define BOMB_H

#include <QObject>

class bomb : public QObject
{
    Q_OBJECT
public:
    explicit bomb(QObject *parent = nullptr);
    bool isset=false; //此炸弹是否已安置
    int SetLocation_X=100;
    int SetLocation_Y=100;

signals:

public slots:
};

#endif // BOMB_H
