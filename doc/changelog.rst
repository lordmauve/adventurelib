Release History
===============

1.2.1 - 2019-10-08
------------------

* Fix: prevent repeating an identifier in a `@when` pattern.
* Minor packaging improvements.

1.2 - 2018-02-13
----------------

* New: Commands can be configured to be active only in certain :ref:`contexts`.
* Fix: ``say()`` function does not dedent before wrapping text.

1.1 - 2016-11-20
----------------

* New: ``say()`` function that eliminates formatting problems in printing
  multi-line prose.
* New: :meth:`get_random()` and :meth:`take_random()` functions to allow
  randomly selecting items from a :class:`Bag`.
* Fix: a bug where ``@when`` statements match even if extra words are given.
* Fix: Bag find/get methods were not properly case-insensitive.


1.0 - 2016-10-01
----------------

Initial public release.
