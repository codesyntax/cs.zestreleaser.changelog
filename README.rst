==========================================
Fill the changelog using VCS's log feature
==========================================


Using the features available at zest.releser.lasttaglog this module
fills the CHANGES file using the VCS's log command.

Actual implementation only works with git. To add support to other VCSs you need to add new conditions to the `prettyfy_logs` method

Developing
===========

Create a virtualenv somewhere::

    $ virtualenv .
    $ source bin/activate

Install zc.buildout::

    $ pip install zc.buildout

Run buildout::

    $ ./bin/buildout -vv

Latest zest.releaser with the developing version of cs.zestreleaser.changelog will be installed and available through all the scripts created in bin folder.
So you can run bin/fullrelease for instance.
