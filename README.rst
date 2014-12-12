==========================================
Fill the changelog using VCS's log feature
==========================================


Using the features available at zest.releser.lasttaglog this module
fills the CHANGES file using the VCS's log command.

Actual implementation only works with git. To add support to other VCSs you need to add new conditions to the `prettyfy_logs` method

