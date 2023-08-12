# -*- coding: utf-8 -*-
"""
Module/Script Name: models
Author: Spring
Date: 29/07/2023
Description: 
"""

from django.db import models


class TimestampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = self.updated_at
        super().save(*args, **kwargs)


class StatusMixin(models.Model):
    is_active = models.BooleanField(default=True, verbose_name='是否启用', auto_created=True)

    class Meta:
        abstract = True


class SoftDeleteMixin(models.Model):
    is_deleted = models.BooleanField(default=False, verbose_name='是否删除')

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save()

    def hard_delete(self, using=None, keep_parents=False):
        super().delete(using=using, keep_parents=keep_parents)


class TimestampStatusMixin(TimestampMixin, StatusMixin, SoftDeleteMixin):
    class Meta:
        abstract = True


def main():
    # function body, if any
    pass


if __name__ == "__main__":
    main()
