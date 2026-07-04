from enemy import Enemy

WAVE_TABLE = [
        [('basic', 10, 0.9)],
        [('basic', 8, 0.8), ('basic', 6, 0.5)],
        [('basic', 6, 0.7), ('basic, 12, 0.3'), ('basic', 2, 2.0)]
        ]
TOTAL_WAVES = len(WAVE_TABLE)
BETWEEN_WAVE_DELAY = 7.0

class WaveManager:
    def __init__(self, pixel_waypoints, enemy_group):
        self.pixel_waypoints = pixel_waypoints
        self.enemy_group = enemy_group

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
