#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: trigger.py


from .base import ProxyCallback, Callback

__all__ = ['PeriodicTrigger', 'PeriodicRunHooks', 'EnableCallbackIf']


class PeriodicTrigger(ProxyCallback):
    """
    Schedule to trigger a callback every k global steps or every k epochs by its ``trigger()`` method.
    """

    _chief_only = False

    def __init__(self, triggerable, every_k_steps=None, every_k_epochs=None):
        """
        Args:
            triggerable (Callback): a Callback instance with a _trigger method to be called.
            every_k_steps (int): trigger when ``global_step % k == 0``. Set to
                None to disable.
            every_k_epochs (int): trigger when ``epoch_num % k == 0``. Set to
                None to disable.

        every_k_steps and every_k_epochs can be both set, but cannot be both None.
        """
        assert isinstance(triggerable, Callback), type(triggerable)
        super(PeriodicTrigger, self).__init__(triggerable)
        assert (every_k_epochs is not None) or (every_k_steps is not None), \
            "every_k_steps and every_k_epochs cannot be both None!"
        self._step_k = every_k_steps
        self._epoch_k = every_k_epochs

    def _trigger_step(self):
        if self._step_k is None:
            return
        if self.global_step % self._step_k == 0:
            self.cb.trigger()

    def _trigger_epoch(self):
        if self._epoch_k is None:
            return
        if self.epoch_num % self._epoch_k == 0:
            self.cb.trigger()

    def __str__(self):
        return "PeriodicTrigger-" + str(self.cb)


class PeriodicRunHooks(ProxyCallback):
    """
    Schedule the ``{before,after}_run`` methods of a callback every k global steps.
    All other methods are untouched.
    """

    _chief_only = False

    def __init__(self, callback, every_k_steps):
        """
        Args:
            callback (Callback):
            every_k_steps(int): call ``{before,after}_run`` when
                ``global_step % k == 0``.
        """
        self._every_k_steps = int(every_k_steps)
        super(PeriodicRunHooks, self).__init__(callback)

    def _before_run(self, ctx):
        if self.global_step % self._every_k_steps == 0:
            self._enabled = True
            return self.cb._before_run(ctx)
        else:
            self._enabled = False

    def _after_run(self, ctx, rv):
        if self._enabled:
            self.cb._after_run(ctx, rv)

    def __str__(self):
        return "PeriodicRunHooks-" + str(self.cb)


class EnableCallbackIf(ProxyCallback):
    """
    Enable ``{before,after}_epoch``, ``{before,after}_run``, ``trigger*``
    methods of a callback, only when some condition satisfies.
    The other methods will be called the same.

    Note:
        If you use ``{before,after}_run``,
        ``pred`` will be evaluated only in ``before_run``.
    """

    _chief_only = False

    def __init__(self, callback, pred):
        """
        Args:
            callback (Callback):
            pred (self -> bool): a callable predicate
        """
        self._pred = pred
        super(EnableCallbackIf, self).__init__(callback)

    def _before_run(self, ctx):
        if self._pred(self):
            self._enabled = True
            return super(EnableCallbackIf, self)._before_run(ctx)
        else:
            self._enabled = False

    def _after_run(self, ctx, rv):
        if self._enabled:
            super(EnableCallbackIf, self)._after_run(ctx, rv)

    def _before_epoch(self):
        if self._pred(self):
            super(EnableCallbackIf, self)._before_epoch()

    def _after_epoch(self):
        if self._pred(self):
            super(EnableCallbackIf, self)._after_epoch()

    def _trigger(self):
        if self._pred(self):
            super(EnableCallbackIf, self)._trigger()

    def _trigger_epoch(self):
        if self._pred(self):
            super(EnableCallbackIf, self)._trigger_epoch()

    def _trigger_step(self):
        if self._pred(self):
            super(EnableCallbackIf, self)._trigger_step()
