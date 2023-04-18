import time
import pygame

pygame.init()

# Open a window
(width, height) = (300, 200)
screen = pygame.display.set_mode((width, height))
pygame.display.flip()

start = None
end = None
# Loop until both keypresses received
while None == end:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Note you had typo here
                if None == start:
                    start = time.time()
                else:
                    end = time.time()
                    print(end - start)

# Close window
pygame.display.quit()
pygame.quit()

#def calculateDaysBetweenDates(begin, end):

# Assign a sequence of integers from 6 to 20 (inclusive) to a NumPy array named feature 

# Create an 3x4 (3 rows x 4 columns) pandas DataFrame
df = pd.DataFrame(np.arange(12).reshape(3, 4))
# the columns are named Eleanor, Chidi, Tahani, and Jason
df.columns = ['Eleanor', 'Chidi', 'Tahani', 'Jason']
# Populate each of the 12 cells in the DataFrame with a random integer between 0 and 100, inclusive
df(data = np.random.randint(0, 100, size=12).reshape(3, 4))
print(df)



#        


