#include "markupform.h"
#include "ui_markupform.h"

MarkupForm::MarkupForm(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::MarkupForm)
{
    ui->setupUi(this);
}

MarkupForm::~MarkupForm()
{
    delete ui;
}
