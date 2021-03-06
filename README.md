# arupcomputepy

This is a library for making calls to [Arup Compute](https://compute.arup.digital/).

Full python documentation can be found [on the ArupCompute documentation site](https://compute.arup.digital/docs/python/).

## Installation

Once you have python installed on your computer, you can install arupcomputepy by calling pip:

`pip install git+ssh://git@github.com/arup-group/arupcomputepy.git`

This will install the latest version of arupcomputepy, run the command again to get up to date.

To check that arupcomputepy has installed correctly and is running try running:

```python
import arupcomputepy
arupcomputepy.test()
```

The expected outcome is

`arupcomputepy has installed correctly`

## Usage

See the [examples](https://github.com/arup-group/arupcomputepy/tree/master/arupcomputepy/Examples) folder

## Authentication

ArupCompute is hosted on the Microsoft Azure cloud computing platform. Authentication is required to prevent outside access to the service. When first running a script that uses arupcomputepy a message will appear in the console prompting you to authorise yourself. Follow the link in the message and use the supplied access code to do this, then log-in with your Arup account. This will save an access token to your hard drive that will be valid for 90 days.

Note that if you do not have an access token saved on your computer, and you cannot see the console, your script will hang indefinitely at this point.
