import pygame
import random
from config import *
from utils import *

class GameMode:
    def __init__(self, screen, mode_name):
        self.screen = screen
        self.mode = mode_name
        self.score = 0
        self.question_index = 0
        self.current_question = None
        self.options = []
        self.feedback_message = ""
        self.feedback_color = BLACK
    
    def draw_header(self, extra_text=""):
        header = f"Score: {self.score} | Soal: {self.question_index+1}"
        if extra_text:
            header += f" | {extra_text}"
        t_head = FONT.render(header, True, BLACK)
        self.screen.blit(t_head, (20, 20))
    
    def draw_question_text(self, text, y=80):
        t_q = FONT.render(text, True, BLACK)
        self.screen.blit(t_q, t_q.get_rect(center=(WIDTH//2, y)))
    
    def draw_feedback(self):
        if self.feedback_message:
            t_feed = FONT.render(self.feedback_message, True, self.feedback_color)
            self.screen.blit(t_feed, (WIDTH//2 - t_feed.get_width()//2, 120))
    
    def draw_grid_options(self):
        mouse_pos = pygame.mouse.get_pos()
        box_w, box_h = 200, 130
        gap_x, gap_y = 40, 40
        start_x = (WIDTH - (2*box_w + gap_x)) // 2
        start_y = 240
        
        for i, country in enumerate(self.options):
            col = i % 2
            row = i // 2
            x = start_x + col*(box_w + gap_x)
            y = start_y + row*(box_h + gap_y)
            rect = pygame.Rect(x, y, box_w, box_h)
            
            border_col = ORANGE if rect.collidepoint(mouse_pos) else BLACK
            
            if country in FLAG_IMAGES:
                img = scale_keep_ratio(FLAG_IMAGES[country], box_w, box_h)
                self.screen.blit(img, (x, y))
            else:
                flag_generic(self.screen, x, y, box_w, box_h)
            
            pygame.draw.rect(self.screen, border_col, rect, 3)
    
    def handle_grid_click(self, pos):
        box_w, box_h = 200, 130
        gap_x, gap_y = 40, 40
        start_x = (WIDTH - (2*box_w + gap_x)) // 2
        start_y = 240
        
        for i, country in enumerate(self.options):
            col = i % 2
            row = i // 2
            x = start_x + col*(box_w + gap_x)
            y = start_y + row*(box_h + gap_y)
            rect = pygame.Rect(x, y, box_w, box_h)
            if rect.collidepoint(pos):
                return country
        return None


class EasyMode(GameMode):
    def __init__(self, screen):
        super().__init__(screen, "EASY")
        self.max_questions = 10
    
    def generate_question(self):
        self.feedback_message = ""
        available = list(FLAG_IMAGES.keys()) if FLAG_IMAGES else ["Indonesia", "Japan"]
        correct = random.choice(available)
        self.current_question = (correct, correct)
        
        remaining = [c for c in available if c != correct]
        distractors = random.sample(remaining, min(3, len(remaining)))
        self.options = [correct] + distractors
        random.shuffle(self.options)
    
    def check_answer(self, answer):
        correct = self.current_question[1]
        if answer == correct:
            self.score += 10
            self.feedback_message = "BENAR!"
            self.feedback_color = GREEN
        else:
            self.feedback_message = f"SALAH! Jawaban: {correct}"
            self.feedback_color = RED
        
        self.question_index += 1
        return "GAMEOVER" if self.question_index >= self.max_questions else "CONTINUE"
    
    def update(self):
        return "CONTINUE"
    
    def draw(self, background):
        if background:
            self.screen.blit(background, (0, 0))
        else:
            self.screen.fill(WHITE)
        
        self.draw_header()
        
        negara = self.current_question[0]
        if negara in FLAG_IMAGES:
            img = scale_keep_ratio(FLAG_IMAGES[negara], 250, 150)
            self.screen.blit(img, (WIDTH//2 - img.get_width()//2, 40))
        else:
            flag_generic(self.screen, WIDTH//2 - 125, 40, 250, 150)
        
        t_soal = FONT.render("Bendera negara apakah ini?", True, BLACK)
        self.screen.blit(t_soal, (WIDTH//2 - t_soal.get_width()//2, 220))
        
        self.draw_feedback()
        
        # Draw vertical options
        mouse_pos = pygame.mouse.get_pos()
        box_w, box_h = 320, 52
        gap_y = 18
        start_x = WIDTH//2 - box_w//2
        start_y = 290
        
        for i, country in enumerate(self.options):
            y = start_y + i*(box_h + gap_y)
            rect = pygame.Rect(start_x, y, box_w, box_h)
            
            bg_color = (255, 255, 255, 200)
            button_surf = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
            pygame.draw.rect(button_surf, bg_color, (0, 0, box_w, box_h), border_radius=20)
            border_col = ORANGE if rect.collidepoint(mouse_pos) else (90, 90, 90)
            pygame.draw.rect(button_surf, border_col, (0, 0, box_w, box_h), 3, border_radius=20)
            self.screen.blit(button_surf, (start_x, y))
            
            text = FONT.render(country, True, BLACK)
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)
    
    def handle_click(self, pos):
        box_w, box_h = 320, 52
        gap_y = 18
        start_x = WIDTH//2 - box_w//2
        start_y = 290
        
        for i, country in enumerate(self.options):
            y = start_y + i*(box_h + gap_y)
            rect = pygame.Rect(start_x, y, box_w, box_h)
            if rect.collidepoint(pos):
                return self.check_answer(country)
        return "CONTINUE"


class ExpertMode(GameMode):
    def __init__(self, screen):
        super().__init__(screen, "EXPERT")
        self.lives = 3
        self.time_left = 20
        self.last_time_update = 0
    
    def generate_question(self):
        self.time_left = 20
        self.last_time_update = pygame.time.get_ticks()
        self.feedback_message = ""
        
        available = list(FLAG_IMAGES.keys()) if FLAG_IMAGES else ["Indonesia", "Japan"]
        
        if DATA_EXPERT:
            for _ in range(50):
                desc, correct = random.choice(DATA_EXPERT)
                if correct in available:
                    self.current_question = (desc, correct)
                    break
            else:
                correct = random.choice(available)
                self.current_question = (f"Deskripsi {correct}", correct)
        else:
            correct = random.choice(available)
            self.current_question = (f"Deskripsi {correct}", correct)
        
        correct_country = self.current_question[1]
        remaining = [c for c in available if c != correct_country]
        distractors = random.sample(remaining, min(3, len(remaining)))
        self.options = [correct_country] + distractors
        random.shuffle(self.options)
    
    def check_answer(self, answer):
        correct = self.current_question[1]
        if answer == correct:
            self.score += 10
            self.feedback_message = "BENAR!"
            self.feedback_color = GREEN
        else:
            self.feedback_message = f"SALAH! Jawaban: {correct}"
            self.feedback_color = RED
            self.lives -= 1
        
        self.question_index += 1
        return "GAMEOVER" if self.lives <= 0 else "CONTINUE"
    
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_time_update > 1000:
            self.time_left -= 1
            self.last_time_update = now
            if self.time_left <= 0:
                self.lives -= 1
                self.feedback_message = "WAKTU HABIS!"
                self.question_index += 1
                return "GAMEOVER" if self.lives <= 0 else "CONTINUE"
        return "CONTINUE"
    
    def draw(self, background):
        if background:
            self.screen.blit(background, (0, 0))
        else:
            self.screen.fill(WHITE)
        
        self.draw_header(f"Time: {self.time_left}")
        draw_lives(self.screen, 20, 60, self.lives)
        self.draw_question_text(self.current_question[0])
        self.draw_feedback()
        self.draw_grid_options()
    
    def handle_click(self, pos):
        answer = self.handle_grid_click(pos)
        if answer:
            result = self.check_answer(answer)
            if result == "CONTINUE":
                self.generate_question()
            return result
        return "CONTINUE"


class TimeMode(GameMode):
    def __init__(self, screen):
        super().__init__(screen, "TIME")
        self.time_left = 60
        self.last_time_update = 0
    
    def generate_question(self):
        self.last_time_update = pygame.time.get_ticks()
        self.feedback_message = ""
        
        available = list(FLAG_IMAGES.keys()) if FLAG_IMAGES else ["Indonesia", "Japan"]
        
        if DATA_EXPERT:
            desc, correct = random.choice(DATA_EXPERT)
            self.current_question = (desc, correct)
        else:
            correct = random.choice(available)
            self.current_question = (f"Deskripsi {correct}", correct)
        
        remaining = [c for c in available if c != correct]
        distractors = random.sample(remaining, min(3, len(remaining)))
        self.options = [correct] + distractors
        random.shuffle(self.options)
    
    def check_answer(self, answer):
        correct = self.current_question[1]
        if answer == correct:
            self.score += 10
            self.feedback_message = "BENAR!"
            self.feedback_color = GREEN
        else:
            self.feedback_message = f"SALAH! Jawaban: {correct}"
            self.feedback_color = RED
        
        self.question_index += 1
        return "CONTINUE"
    
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_time_update > 1000:
            self.time_left -= 1
            self.last_time_update = now
            if self.time_left <= 0:
                return "GAMEOVER"
        return "CONTINUE"
    
    def draw(self, background):
        if background:
            self.screen.blit(background, (0, 0))
        else:
            self.screen.fill(WHITE)
        
        self.draw_header()
        header2 = f"Time: {self.time_left}"
        t_head2 = FONT.render(header2, True, BLACK)
        self.screen.blit(t_head2, (20, 55))
        
        self.draw_question_text(self.current_question[0])
        self.draw_feedback()
        self.draw_grid_options()
    
    def handle_click(self, pos):
        answer = self.handle_grid_click(pos)
        if answer:
            result = self.check_answer(answer)
            if result == "CONTINUE":
                self.generate_question()
            return result
        return "CONTINUE"


class SurvivalMode(GameMode):
    def __init__(self, screen):
        super().__init__(screen, "SURVIVAL")
        self.lives = 3
    
    def generate_question(self):
        self.feedback_message = ""
        
        available = list(FLAG_IMAGES.keys()) if FLAG_IMAGES else ["Indonesia", "Japan"]
        
        if DATA_EXPERT:
            desc, correct = random.choice(DATA_EXPERT)
            self.current_question = (desc, correct)
        else:
            correct = random.choice(available)
            self.current_question = (f"Deskripsi {correct}", correct)
        
        remaining = [c for c in available if c != correct]
        distractors = random.sample(remaining, min(3, len(remaining)))
        self.options = [correct] + distractors
        random.shuffle(self.options)
    
    def check_answer(self, answer):
        correct = self.current_question[1]
        if answer == correct:
            self.score += 10
            self.feedback_message = "BENAR!"
            self.feedback_color = GREEN
        else:
            self.feedback_message = f"SALAH! Jawaban: {correct}"
            self.feedback_color = RED
            self.lives -= 1
        
        self.question_index += 1
        return "GAMEOVER" if self.lives <= 0 else "CONTINUE"
    
    def update(self):
        return "CONTINUE"
    
    def draw(self, background):
        if background:
            self.screen.blit(background, (0, 0))
        else:
            self.screen.fill(WHITE)
        
        self.draw_header()
        draw_lives(self.screen, 20, 60, self.lives)
        self.draw_question_text(self.current_question[0])
        self.draw_feedback()
        self.draw_grid_options()
    
    def handle_click(self, pos):
        answer = self.handle_grid_click(pos)
        if answer:
            result = self.check_answer(answer)
            if result == "CONTINUE":
                self.generate_question()
            return result
        return "CONTINUE"