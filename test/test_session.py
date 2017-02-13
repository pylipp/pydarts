import unittest

from pydarts.session import Player


class PlayerEntryTestCase(unittest.TestCase):
    def setUp(self):
        self.player = Player("Raymond", 0, 501)

    def test_not_victorious(self):
        self.assertFalse(self.player.victorious())

    def test_scores_valid(self):
        self.assertTrue(self.player.score_valid(180))
        self.player._visit.append(60)
        self.assertFalse(self.player.score_valid(121))
        # hack low remaining score
        self.player._score_left = 40
        self.assertTrue(self.player.score_valid(20))
        # busted
        self.assertFalse(self.player.score_valid(39))
        self.assertFalse(self.player.score_valid(42))
        # finish
        self.assertTrue(self.player.score_valid(40))

    def test_substract(self):
        # first visit
        self.player.substract(180, True)
        self.assertEqual(self.player.score_left, 321)
        self.assertEqual(self.player.throws, 3)
        self.assertEqual(self.player.darts, 0)
        self.assertEqual(self.player.visit_sum(), 180)
        # second visit
        self.player.begin()
        self.assertEqual(self.player.visit_sum(), 0)
        self.assertEqual(self.player.darts, 3)
        self.player.substract(60, False)
        self.assertEqual(self.player.throws, 4)
        self.assertEqual(self.player.darts, 2)
        self.player.substract(60, False)
        self.player.substract(60, False)
        self.assertEqual(self.player.throws, 6)
        self.assertEqual(self.player.darts, 0)
        self.assertEqual(self.player.visit_sum(), 180)
        self.assertEqual(self.player.score_left, 141)
        # third visit, busting for testing reasons
        self.player.begin()
        self.player.substract(0, True)
        self.assertEqual(self.player.throws, 9)
        self.assertEqual(self.player.score_left, 141)
        # fourth visit, busts again
        self.player.begin()
        self.player.substract(60, False)
        self.assertEqual(self.player.score_left, 81)
        self.player.substract(-60, True)
        self.assertEqual(self.player.throws, 12)
        self.assertEqual(self.player.score_left, 141)
        # fifth visit, finishes
        self.player.begin()
        self.player.substract(141, True)
        self.assertEqual(self.player.throws, 15)
        self.assertTrue(self.player.victorious())

    def test_process_score(self):
        self.assertTupleEqual(self.player._process_score("99d"), (99, True))
        self.assertTupleEqual(self.player._process_score("60"), (60, False))
        # bust (score is actually impossible, returns 0 because substract() not called)
        self.assertTupleEqual(self.player._process_score("b"), (0, True))
        self.assertRaises(ValueError, self.player._process_score, "200")
        self.assertRaises(ValueError, self.player._process_score, "hi")

    def test_play(self):
        self.player.play("60", "60", "60")
        self.assertEqual(self.player.score_left, 321)
        self.assertEqual(self.player.darts, 0)
        self.player.play("180")
        self.assertEqual(self.player.score_left, 141)
        self.assertEqual(self.player.darts, 0)
        self.player.play("1", "20", "d")
        self.assertEqual(self.player.score_left, 120)
        self.assertEqual(self.player.darts, 0)
        self.player.play("20d")
        self.assertEqual(self.player.score_left, 100)
        self.assertEqual(self.player.darts, 0)
        self.assertRaises(ValueError, self.player.play, "60", "60")
        self.assertEqual(self.player.score_left, 40)
        self.assertEqual(self.player.darts, 2)
        # bypass begin() when calling play(), because it would log the first 60 abcve
        score, is_total = self.player._process_score("b")
        self.player.substract(score, is_total)
        self.assertEqual(self.player.score_left, 100)
        self.assertEqual(self.player.darts, 0)
        self.assertRaises(ValueError, self.player.play, "darts<3")
        self.assertEqual(self.player.darts, 3)
        self.player.play("50", "50")
        self.assertTrue(self.player.victorious())


if __name__ == '__main__':
    unittest.main()
