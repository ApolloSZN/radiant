# ADR-003: Forecast model selection is prequential

Status: Accepted.

The sequencing regime shift made fixed-history models fail, while forced adaptation harmed the battery domain. Radiant therefore selects among memory lengths using only errors observed before the target being predicted. Current-target outcomes cannot alter the model chosen for that target.
