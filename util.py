
def check_wall_collision(rect, walls):
    for wall in walls:
        if(rect.colliderect(wall)):
            return True
    
    return False