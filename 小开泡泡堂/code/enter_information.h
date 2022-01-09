#ifndef ENTER_INFORMATION_H
#define ENTER_INFORMATION_H
#include<QCloseEvent>
#include <QWidget>
#include<QDialog>
#include<QMessageBox>
#include"pausesave.h"
namespace Ui {
class Enter_Information;
}

class Enter_Information : public QDialog
{
    Q_OBJECT

public:
    explicit Enter_Information( QDialog *parent = nullptr);
    ~Enter_Information();

private slots:
    void on_confirm_clicked();//输入后的响应按钮
private:
    Ui::Enter_Information *ui;//输入框的设计界面
};

#endif // ENTER_INFORMATION_H
