#ifndef MARKUPFORM_H
#define MARKUPFORM_H

#include <QWidget>

namespace Ui {
class MarkupForm;
}

class MarkupForm : public QWidget
{
    Q_OBJECT

public:
    explicit MarkupForm(QWidget *parent = 0);
    ~MarkupForm();

private:
    Ui::MarkupForm *ui;
};

#endif // MARKUPFORM_H
