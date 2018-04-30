1.10.1
======

Packaging refresh. Docs now published in RTD.

1.10
====

FoldedCase now supports string-containment support in an
unfortunately assymetric way.

1.9.2
=====

Fix bug where ``FoldedCase.__ne__`` was case-sensitive.

1.9.1
=====

Refresh packaging.

1.9
===

Synchronize with skeleton.

Update docs and expand tests on FoldedCase.

Use method_cache for ``FoldedCase.lower``.

1.8
===

Add remove_prefix and remove_suffix helpers.

1.7
===

In Stripper, always strip the prefix, even if it's empty.

1.6.2
=====

Issue #1: Fix WordSet on Python 2.

1.6
===

Drop dependency on jaraco.context (and its dependencies).

1.5
===

Move hosting to github.

Add missing namespace package declaration in distribution.

1.4
===

Add Stripper class.

1.3
===

Add SeparatedValues class.

1.0
===

Initial implementation adopted from jaraco.util.string 10.8.
