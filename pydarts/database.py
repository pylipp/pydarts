import os.path
import time
from collections import Counter
from abc import ABCMeta

from tinydb import TinyDB, where
from lxml import etree


class LogEntryBase(object):
    """Abstract base class for all classes that are supposed to support
    logging.

    It holds a member `_log_entry` of type `lxml.etree._Element`. Its tag is
    derived from the lowercase class name. If a `parent` argument (an instance
    of a class that implements an `append` method, such as a list or this
    class) is passed, the `log_entry` is appended, s.t. the hierarchy of the
    `session` classes is reflected in the XML log.
    The initialization time of each instance is stored as timestamp for later
    reference.
    """

    __metaclass__ = ABCMeta

    DT_FORMAT = "%Y%m%d-%H%M%S"

    def __init__(self, parent=None):
        tag = self.__class__.__name__.lower()
        self._log_entry = etree.Element(tag,
                attrib={"timestamp": time.strftime(self.DT_FORMAT)})
        if parent is not None:
            parent.append(self._log_entry)

    def append(self, child_log_entry):
        self._log_entry.append(child_log_entry)


class PlayerEntry(object):

    def __init__(self, name=None, player_stats=None):
        self._name = name
        self._throws = 0
        self._points = 0
        self._finishes = Counter()

        if player_stats:
            self._throws = player_stats["throws"]
            self._points = player_stats["points"]
            self._finishes = player_stats["finishes"]

    def update(self, throws, points, finished=False):
        self._throws += throws
        self._points += points
        if finished:
            self._finishes[throws] += 1

    def to_dict(self):
        return {
                self._name: dict(
                    throws=self._throws,
                    points=self._points,
                    finishes=self._finishes
                    )
                }

    def average(self):
        if self._throws != 0:
            return self._points / self._throws
        return 0


def add(field, value):
    """Operation to increment `field` of a `tinydb.Element` by `value`. The
    field is created if it does not exist."""
    def transform(element):
        if field in element:
            element[field] += value
        else:
            element[field] = value

    return transform


class Stats(TinyDB):
    """Keep track of player and session statistics.
    Pass a list of player names at initialization. New player entries are
    created if they don't exist in the database yet.
    An optional filepath can be passed which is convenient for testing. By
    default, the file `data/stats.json` is used.
    This class is an extension of `tinydb.TinyDB`."""

    def __init__(self, player_names=[], filepath=None):
        self._filepath = filepath
        if self._filepath is None:
            dirname = os.path.dirname(os.path.abspath(__file__))
            self._filepath = os.path.join(dirname, "..", "data", "stats.json")
        super().__init__(self._filepath)

        for name in player_names:
            if not self.table("players").get(where("name") == name):
                self.table("players").insert({"name": name})

    def update(self, player=None):
        """Update information about player performance. Should be called after
        a player's visit."""
        if player is not None:
            stats = {
                    "throws": 3 - player.darts,
                    "points": player.visit_sum()
                    }
            if player.victorious():
                stats["finish_{:03}".format(stats["points"])] = 1

            for k, v in stats.items():
                self.table("players").update(
                        add(k, v), where("name") == player.name)
