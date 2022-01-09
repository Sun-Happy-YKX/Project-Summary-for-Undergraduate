#include "mainwindow.h"
#include <QApplication>
#include"start.h"
#include"endshow.h"
int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    QString path=QApplication::applicationDirPath();
    path+="/img/favicon.ico";
    a.connect( &a,SIGNAL(lastWindowClosed()),&a,SLOT(quit()));//他保证了程序能合理的退出
    a.setWindowIcon(QIcon(path));//添加图标
    QApplication::setQuitOnLastWindowClosed(false);
    Start S;
    S.show();
    return a.exec();
}
