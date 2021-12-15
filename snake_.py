import random

import arcade

class Pear(arcade.Sprite):
    def __init__(self, w, h):
        arcade.Sprite.__init__(self)
        self.img = 'img/pear.jpg'
        self.pear = arcade.Sprite(self.img , 0.09)
        self.center_x = random.randint(0, w)
        self.center_y = random.randint(0, h)

    def draw(self):
        self.pear.draw()

class Chocolate(arcade.Sprite):
    def __init__(self, w, h):
        arcade.Sprite.__init__(self)
        self.img = 'img/choco.jpg'
        self.choco = arcade.Sprite(self.img , 0.09)
        self.center_x = random.randint(0, w)
        self.center_y = random.randint(0, h)

    def draw(self):
        self.choco.draw()        

class Apple(arcade.Sprite):
    def __init__(self, w, h):
        arcade.Sprite.__init__(self)
        self.img = 'img/apple.jpg'
        self.apple = arcade.Sprite(self.img , 0.09)
        self.center_x = random.randint(0, w)
        self.center_y = random.randint(0, h)

    def draw(self):
        self.apple.draw()
        
class Snake(arcade.Sprite):
    def __init__(self, w, h):
        arcade.Sprite.__init__(self)
        self.color = arcade.color.SEA_GREEN
        self.speed = 3
        self.width = 16
        self.height = 16
        self.center_x = w // 2
        self.center_y = h // 2
        self.r = 8
        self.change_x = 0
        self.change_y = 0
        self.score = 0
        self.body = []
        self.body.append([self.center_x, self.center_y])

    def draw(self):        
        for i in range(len(self.body)):
            if i % 3 == 0:
                arcade.draw_circle_filled(self.body[i][0], self.body[i][1], self.r, self.color)
            elif i % 3 == 1:
                arcade.draw_circle_filled(self.body[i][0], self.body[i][1], self.r, arcade.color.RED)
            else:
                arcade.draw_circle_filled(self.body[i][0], self.body[i][1], self.r, arcade.color.YELLOW_ROSE)
       
    def move(self,x_apple,y_apple):
        if self.center_x<x_apple:
            self.change_x=1
        elif self.center_x>x_apple:
            self.change_x=-1
        elif self.center_x==x_apple:
            self.change_x=0

        if self.center_y<y_apple:
            self.change_y=1
        elif self.center_y>y_apple:
            self.change_y=-1
        elif self.center_y==y_apple:
            self.change_y=0

        self.center_x += self.speed * self.change_x
        self.center_y += self.speed * self.change_y
        self.body.append([self.center_x , self.center_y])

        if len(self.body)>1:
            del self.body[0]


    def eat(self , n):
        if n == 'apple':
            self.score += 1
        elif n == 'pear':
            self.score += 2
        elif n == 'chocolate':
            self.score -= 1 
  

class Game(arcade.Window):
    def __init__(self):
        arcade.Window.__init__(self, 600, 500, 'Snake Game')
        arcade.set_background_color(arcade.color.PURPLE_TAUPE)
        self.snake = Snake(600, 500)
        self.apple = Apple(600, 500)
        self.pear = Pear(600, 500)
        self.chocolate = Chocolate(600, 500)
        self.game_over=GameOver()
        self.flag=0

    def on_draw(self):
        #نمایش اشیاء داخل بازی 
        arcade.start_render()
        self.snake.draw()
        self.apple.draw()
        self.pear.draw()
        self.chocolate.draw()

        arcade.draw_text('Score: %i'%self.snake.score, start_x= 10, start_y= 10,
          color= arcade.color.PINK, font_size = 20)

        if self.flag==1:
            self.game_over.on_draw()

    def on_update(self, delta_time: float):
        #تمام منطق و اتفاقات بازی این تابع رخ میده
        self.snake.move(self.apple.center_x , self.apple.center_y)
        if arcade.check_for_collision(self.snake, self.apple):
            self.snake.eat('apple')
            self.snake.body.append([self.snake.body[len(self.snake.body)-1][0],
             self.snake.body[len(self.snake.body)-1][1]])
            self.apple = Apple(600, 500)
            print(self.snake.score)

        elif arcade.check_for_collision(self.snake, self.pear):
            self.snake.eat('pear')
            self.snake.body.append([self.snake.body[len(self.snake.body)-1][0],
             self.snake.body[len(self.snake.body)-1][1]])
            self.pear = Pear(600, 500)
            print(self.snake.score)

        elif arcade.check_for_collision(self.snake, self.chocolate):
            self.snake.eat('chocolate')
            if self.snake.score <= 0:
                self.flag=1
            self.chocolate = Chocolate(600, 500)
            del self.snake.body[-1]
            print(self.snake.score)

    def on_key_release(self, key):
        #هرتابعی روی کیبورد فشرده شود و سپس رها بشه این تابع اجرا میشه
        if key == arcade.key.LEFT:
            self.snake.change_x = -1
            self.snake.change_y = 0

        elif key == arcade.key.RIGHT:
            self.snake.change_x = +1
            self.snake.change_y = 0

        elif key == arcade.key.UP:
            self.snake.change_x = 0
            self.snake.change_y = +1
        
        elif key == arcade.key.DOWN:
            self.snake.change_x = 0
            self.snake.change_y = -1



class GameOver(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.PURPLE_TAUPE)
        arcade.set_viewport(0,600-1,0,500-1)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text('Game Over',600//2.4 , 500//2 ,arcade.color.PINK,20,20)
        arcade.draw_text('Press ESC for exit ',600//2.4 , 500//2.3 ,arcade.color.PINK,12,12)

    def exit_game(self):
        arcade.finish_render()
        arcade.exit()
        
   

game = Game()
arcade.run()
        