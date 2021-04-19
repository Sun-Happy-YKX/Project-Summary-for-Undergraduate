#ifndef START_H
#define START_H

#include <QWidget>
#include<QLabel>
#include<QPushButton>
#include"mainwindow.h"

class Start : public QWidget
{
    Q_OBJECT
public:
    explicit Start(QWidget *parent = nullptr);
    MainWindow *w;
private:
    QLabel *label;
    QPushButton *button[3];


signals:

public slots:
};

#endif // START_H
