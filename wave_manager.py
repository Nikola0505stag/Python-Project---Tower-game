from enemy import Enemy

WAVE_TABLE = [
        [('basic', 10, 0.9)],
        [('basic', 8, 0.8), ('fast', 4, 0.5)],
        [('basic', 6, 0.7), ('swarm', 12, 0.3), ('tank', 1, 2.0)],
        [('fast', 8, 0.4), ('basic', 6, 0.7), ('swarm', 10, 0.25), ('tank', 2, 2.0)],
        [('armored', 6, 0.9), ('fast', 6, 0.4), ('swarm', 15, 0.2)],
        [('basic', 12, 0.5), ('armored', 4, 0.8), ('regen', 3, 2.5), ('tank', 2, 1.8)],
        [('tank', 10, 0.35), ('armored', 6, 0.75), ('regen', 4, 2.0), ('tank', 2, 2.0)],
        [('basic', 8, 0.5), ('split', 4, 1.5), ('tank', 3, 1.8), ('boss', 1, 0)],
        [('armored', 6, 0.6), ('split', 6, 1.2), ('fast', 10, 0.3), ('regen', 3, 2.5)],
        [('ghost', 5, 1.5), ('fast', 12, 0.3), ('armored', 8, 0.5), ('boss', 1, 4.0)],
        [('ghost', 6, 1.2), ('swarm', 20, 0.2), ('armored', 10, 0.55), ('fast', 12, 0.3)],
        [('tank', 6, 1.2), ('regen', 5, 2.0), ('boss', 2, 5.0), ('armored', 8, 0.5)],
        [('ghost', 8, 1.0), ('split', 8, 1.0), ('fast', 16, 0.28), ('tank', 5, 1.2)],
        [('armored', 10, 0.45), ('ghost', 6, 1.2), ('regen', 6, 2.0), ('boss', 2, 4.0), ('tank', 5, 1.5)],
        [('swarm', 25, 0.15), ('ghost', 8, 1.0), ('split', 6, 1.0), ('fast', 15, 0.25),
         ('armored', 12, 0.4), ('tank', 6, 1.0), ('boss', 3, 3.5)]
        ]
TOTAL_WAVES = len(WAVE_TABLE)
BETWEEN_WAVE_DELAY = 7.0

class WaveManager:
    def __init__(self, pixel_waypoints, enemy_group):
        self.pixel_waypoints = pixel_waypoints
        self.enemy_group = enemy_group

        self.TOTAL_WAVES = TOTAL_WAVES

        self.current_wave = 0
        self.state = 'waiting'
        self._wait_timer = BETWEEN_WAVE_DELAY
        self._batch_index = 0
        self._batch_count = 0
        self._spawn_timer = 0.0
        self._current_batches = []

    @property
    def wave_number(self):
        return self.current_wave + 1

    @property
    def wait_seconds_left(self):
        return max(0, self._wait_timer)

    def all_waves_done(self):
        return self.state == 'finished'

    def skip_wait(self):
        if self.state == 'waiting':
            self._wait_timer = 0

    def _start_wave(self):
        self._current_batches = list(WAVE_TABLE[self.current_wave])
        self._batch_index = 0
        self._batch_count = 0
        self._spawn_timer = 0.0
        self.state = 'spawning'
    
    def _spawn_enemy(self, enemy_type):
        enemy = Enemy(enemy_type, self.pixel_waypoints)
        self.enemy_group.add(enemy)

    def update(self, dt):
        if self.state == 'finished':
            return

        if self.state == 'waiting':
            self._wait_timer -= dt
            if self._wait_timer <= 0:
                self._start_wave()
            return

        if self.state == 'spawning':
            self._spawn_timer -= dt
            if self._spawn_timer <= 0:
                if self._batch_index >= len(self._current_batches):
                    self.state = 'in_wave'
                    return

                enemy_type, count, interval = self._current_batches[self._batch_index]
                self._spawn_enemy(enemy_type)
                self._batch_count += 1

                if self._batch_count >= count:
                    self._batch_index += 1
                    self._batch_count = 0
                    self._spawn_timer = interval + 0.5
                else:
                    self._spawn_timer = interval

        if self.state == 'in_wave':
            if self.enemy_group.is_empty():
                self.current_wave += 1
                if self.current_wave >= TOTAL_WAVES:
                    self.state = 'finished'
                else:
                    self._wait_timer = BETWEEN_WAVE_DELAY
                    self.state = 'waiting'
