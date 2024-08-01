# Personal notes

This are my personal thoughts, ideas that came up while I was doing the challenge...
They can be messy, and are not meant to be documentation, just my personal thoughts and reasoning that I would normally think out laud if we were doing a Pair Programming exercise...

## Enums specification

I usually prefer to have Enum's values more descriptive like this:

```python

    class ValidationStatus(models.TextChoices):
        FAILED = "F", _("Failed")
        NOT_VALIDATED = "U", _("Not validated")
        VALIDATED = "V", _("Validated")

```

Where the value "FAILED" correspond to the descriptive value, instead of just "F"
that's because in the code so I can write `ValidationStatus.FAILED` that is more descriptive...

In this solution there are many choices though and this is not always possible, at least
it's hard to define a name in these cases:

```python
    class ReadingType(models.TextChoices):
        A = "A", _("Actual Change of Supplier Read")
        C = "C", _("Customer own read")
        D = "D", _(
            "Deemed (Settlement Registers) or Estimated (Non-Settlement Registers)"
        )
        F = "F", _("Final")
        I = "I", _("Initial")
        M = "M", _("MAR")
        O = "O", _("Old Supplier's Estimated CoS Reading")
        P = "P", _("Electronically collected via PPMIP")
        Q = "Q", _("Meter Reading modified manually by DC")
        R = "R", _("Routine")
        S = "S", _("Special")
        T = "T", _("Proving Test Reading")
        U = "U", _("Forward Migration CoA")
        V = "V", _("Forward Migration CoS")
        W = "W", _("Withdrawn")
        X = "X", _("Supplier Agreed Switch Read")
        Y = "Y", _("Reverse Migration CoS")
        Z = "Z", _("Actual Change of Tenancy Read")

```

Here the value corrisponds to the letter aka not the description...
So there is a bit of inconsistency, but also the descriptive value are long and verbose and I should take some time to decide what is the most readable value...

So there is a bit of inconsistency in here, a little bit... but it's okay for now...

same here:

```python

    class Method(models.TextChoices):
        N = "N", _("Not viewed by an Agent or Non Site Visit")
        P = "P", _("Viewed by an Agent or Site Visit")

```

## Commands

The command to import flow will also be used by the api, so we need to put the logic separate so it can be called by the command and by some views/api indipendently.

I will assume we want to import multiple files in one shot, not one by one, or specify different commands.
If we submit multiple file in the same command how do we recoginse which is which?
The first or last line maybe>

yes the first line has the "D0010002" aka indicates think (where is documented?) the flow and flow version:

Flow Reference:
D0010
Flow Version:
002

Okay the other stuff in the first / last line I don't know what they are for, cannot find in the docs only..
there is a date though

the only thing is theat the command will search for a fisical file in the local file sysetm , the api with a file upload guess will get the name and the content separatly...

## Multiple files

need to open the content , get the first line and the flow reference and version and check if it's supported
would be cool doing it in python just match if there is the class DOO10OO2 and it's done...

## Format of the file discrepancy...

This is the format taht according to the documentation the 030 line should have:

030 Register Readings
0-\*
J0010 Meter Register Id
J0016 Reading Date & Time
J0040 Register Reading
J0044 MD Reset Date & Time
J1013 Number of MD Resets
J0045 Meter Reading Flag
J1888 Reading Method

so the first field after the 030 should be the "register reading" aka the serial number so Meter.register_id ... but in the file:

030|01|20160228000000|88285.0|||T|N|

it's just a two char number/letters... it's not matching a register_id... so wtf?
