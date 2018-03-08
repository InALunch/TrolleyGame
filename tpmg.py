import random 
import time 

class Game:
    def __init__(self):
        self.points = {'kantpoints' : 0, 'utils' : 0}
        self.dilemmas = [TrolleyProblem]
        self.count = 0
        self.weights = [1]
      
    def play(self):
        self.count += 1
        d = self.create_dilemma()
        d.play()
        self.change_scores(d.pointchange)
        time.sleep(2)
        self.print_count()
        self.print_score()
        self.update_dilemmas()
        self.quit()
        time.sleep(1)
        self.play()
    
    def create_dilemma(self):
        gamenum = random.choices(range(len(self.dilemmas)), weights = self.weights)[0]
        gametype = self.dilemmas[gamenum]
        dilem = gametype()
        self.weights[gamenum] *= dilem.entropy
        return dilem

    def update_dilemmas(self):
        if self.count == 1:
            self.dilemmas.append(FatMan)
            self.weights.append(1)
        if self.count == 3:
            self.dilemmas.append(MurdererLiar)
            self.weights.append(1)
        dilemmas = [HarambeTrolley, BookTrolley, DrowningChild]
        if self.count == 5:
            for dilemma in dilemmas:
                self.dilemmas.append(dilemma)
                self.weights.append(1)
            
    
    def change_scores(self, changes):
        for key in changes:
            self.points[key] = self.points.get(key, 0) + changes[key]
            self.points[key] = round(self.points.get(key, 0), 3)
    
    def print_results(self):
        self.print_count()
        self.print_score()
        
    def print_count(self):
        print("\nYou have encountered " + str(self.count) + ' ethical dilemmas.')
        
    def print_score(self):
        for key in self.points:
            print(' '.join(["You have "+ str(self.points[key]), key]))
    
    def quit(self):
        print(' ')
        keep = input("Do you want to keep playing? [Y/N] ")
        if len(keep) == 0 or keep[0].lower() in ["y", "c", "t"]:
            print("Alright, let's keep going.")
        else:
            print("Life is a series of trolley problems. You cannot avoid them.")
        print(' ')
          
class Dilemma:
    #Should not be invoked directly
    def __init__(self):
        self.pointchange = {'utils' : 0, 'kantpoints': 0}
        self.decisionmsg = ''
        self.entropy = .7
    
    def play(self):
        self.print_dilemma()
        time.sleep(1)
        move = self.io()
        self.print_decision(move)
        self.update_scores(move)

    def print_dilemma(self):
        pass
    
    def print_decision(self, move):
        pass
      
    def update_scores(self, move):
        pass
    
    def io(self):
        choice = input(self.decisionmsg)
        legalchoices = set(['p','y','t','s','f','n'])
        while len(choice) == 0 or choice[0].lower() not in legalchoices:
            print ("I didn't catch that...You HAVE to make a choice.")
            choice = input(self.decisionmsg)
        pull = False
        if choice[0].lower() in ['p','y','t','s']:
            pull = True
        return pull
        
    def kant_default(self):
        print("The dilemma is not your problem. On Kantian grounds, that is enough.")
        print("There is no change in your Kant points. #NotYourProblem.")
        self.pointchange['kantpoints'] = 0      

class AbstractTrolley(Dilemma):
    def __init__(self):
        Dilemma.__init__(self)
        self.uppertrack = None
        self.lowertrack = None
        self.lowertracktext = ""
        self.uppertracktext = ""
        self.decisionmsg = "Do you pull the lever? [Y/N] "
        
    def print_dilemma(self):
        print("A runaway trolley is barrelling towards "+ self.lowertracktext)
        print("You can pull a lever to divert the trolley to another track, containing "+ self.uppertracktext)
        print('')
    
    def print_decision(self, move):
        time.sleep(1)
        if move:
            print("You have pulled the lever.\n")
        else:
            print("You let the lever be.\n")


class TrolleyProblem(AbstractTrolley):
    def __init__(self):
        AbstractTrolley.__init__(self)
        self.uppertrack = random.randint(0,5)
        self.lowertrack = random.randint(1,10)
        self.make_text()
    
    def make_text(self):
        self.lowertracktext = str(self.lowertrack) + ' workers who are mysteriously tied up. '
        self.uppertracktext = str(self.uppertrack) + ' workers who are also tied up. '
    
    def update_scores(self, move):
        diff = self.lowertrack - self.uppertrack
        if self.uppertrack == self.lowertrack:
            print("Your choice is neutral on utilitarian grounds")
            self.pointchange['utils'] = 0
        elif (diff < 0 and move )or (diff > 0 and not move):
            print ("You have made the wrong utilitarian decision. Lose "+ str(abs(diff)) + ' utils!')
            self.pointchange['utils'] = - abs(diff)
        elif (diff > 0 and move) or (diff < 0 and not move):
            print("You have made the correct utilitarian decision and saved "+ str(abs(diff)) + " lives.")
            print("Gain "+ str(abs(diff))+ ' utils!')
            self.pointchange['utils'] = abs(diff)
        print('')
        time.sleep(.5)
        
        if not move:
            self.kant_default() 
        elif move and diff > 0:
            print("You have a hypothetical imperative to save lives, but not a categorical one.")
            print("Gain 1 Kant point")
            self.pointchange["kantpoints"] = 1
        else:
            print("You are a MURDERER who have violated the categorical imperative!")
            print("Lose 10 Kant points.")
            self.pointchange["kantpoints"] = -10
        
        time.sleep(.5)
            
class FatMan(Dilemma):
    def __init__(self):
        Dilemma.__init__(self)
        self.decisionmsg = "Do you push the fat man? [Y/N] "
        self.workers = random.randint(0,4)
        

    def print_dilemma(self):
        print("You are standing on top of a bridge.")
        if self.workers > 0:
            print("You see a runaway trolley heading towards " + str(self.workers) + ' very skinny railway workers.')
            print("It is very loud and they will not be able to hear you shouting for them to get off the tracks.\n")
        else:
            print("Below, you see a trolley going down the tracks.")
        time.sleep(1)
        print("There is a very fat and oblivious man standing next to you.")
        print("You believe that if you push him, you can stop the trolley.")
        print('')

    
    def print_decision(self, move):
        if move:
            print("You pushed the fat man and successfully stopped the trolley.")
        else:
            print("You did not push the fat man.")
      
    def update_scores(self, move):
        diff = self.workers - 1
        if move:
            if diff < 0:
                print("You are a MURDERER who have pushed a fat man for no apparent reason.")
                print("Lose 1 util")
            elif diff == 0:
                print("You are a MURDERER who just killed an innocent man in cold blood. On the other hand, there was no net change in lives. So, whatever.")
                print("Lose 0 utils")
            else:
                print("You have made the correct utilitarian choice, saving a net "+str(diff)+' lives.')
                print("Gain %s utils" % (str(diff)))
            self.pointchange['utils'] = diff
        else:
            if diff <= 0:
                print("You have made the right utilitarian choice.")
                print("Gain %s utils" % (-diff))
            else:
                print("In not wanting to get your hands wet, you have killed a net %s lives" %(diff))
                print ("Lose %s utils" %(diff))
            self.pointchange['utils'] = -diff
            
        print('')
        time.sleep(.5)
        if move:
            print("You are a MURDERER who have violated the categorical imperative!")
            print("Lose 10 Kant points.")
            self.pointchange["kantpoints"] = -10
        else:
            self.kant_default() 
    
class MurdererLiar(Dilemma):
    def __init__(self):
        Dilemma.__init__(self)
        self.decisionmsg = "Do you tell the axe murderer where your friends are hiding? [Y/N] "
        self.friends = random.randint(2, 10)
        self.entropy = .1
    
    def print_dilemma(self):
        print( "There's been a rampage of mass murders lately.")
        time.sleep(1)
        print( "School shootings, innocents kidnapped and tied to train tracks, and so forth.")
        time.sleep(2)
        print ("Fortunately, you live in a house with very secure walls.")
        time.sleep(2)
        print("During an extremely bad weekend, %s of your friends are especially worried, and you offer to hide them in your basement." % (self.friends))
        time.sleep(3.5)
        print('')
        print("Your doorbell rang. Thinking that it might be another of your friends, you open the door, only to be greeted by a well-dressed man of large stature.")
        time.sleep(3)
        print("He is holding an axe. A humonguous, jagged, very bloody axe.")
        time.sleep(2)
        print("He informs you that he's going around houses killing people, and proceeds to describe all of your friends downstairs.")
        time.sleep(2.5)
        print("He asks you where your friends are.")
        time.sleep(1)
        print('')
        
    
    def print_decision(self, move):
        if move:
            print("You tell the murderer where your friends are.")
            print("He politely thanks you, and charges down to your basement.")
            time.sleep(3)
            print(' ')
            print("You hear some thuds, and lots of screaming.")
            print("The murderer runs back upstairs, thanks you, and heads off on his merry way.")
            time.sleep(2)
            print('')
            print("%s of your friends are dead!" % (self.friends))
            print("")
            print("You feel bad about your friends dying, but glad that you did not lie.")
            print('')
        else:
            print("You lie through your teeth, and tell the murderer that you haven't seen those people in months.")
            print("")
            print("He politely thanks you and leaves.")
            print('')
            time.sleep(2)
            print("You feel bad about lying, but glad that your friends didn't die.")
            print('')
      
    def update_scores(self, move):
        if move:
            print("By not lying, you allowed the murderer to discern the location of your friends.")
            time.sleep(1)
            print("You are consequentially indistinguishable from a murderer.")
            time.sleep(1)
            print("Lose %s utils" % (self.friends))
            self.pointchange['utils'] = -self.friends
        else:
            print("By mere prevarication, you prevented several of your friends from dying. You should feel really good about yourself!")
            time.sleep(2)
            print ("Gain %s utils" % (self.friends))
            self.pointchange['utils'] = self.friends
        time.sleep(1)
        print('')
        if move:
            print("Saving lives is a hypothetical imperative, while avoiding lying is a categorical imperative.")
            time.sleep(1)
            print("You managed to avoid lying even when it was difficult, treating the rational being in front of you as an end rather than just a means. ")
            time.sleep(2)
            print("You have followed the categorical imperative, not because it's easy, but because it is right.")
            time.sleep(2)
            print("Gain 10 Kant points!")
            self.pointchange['kantpoints'] = 10 
        else:
            print("Saving lives is a hypothetical imperative, while avoiding lying is a categorical imperative.")
            time.sleep(1)
            print("In saving your friends, you've treated the polite murderer as a means rather than an end. You are A LIAR who has violated the categorical imperative!")
            time.sleep(2)
            print("Lose 10 Kant points!")
            self.pointchange['kantpoints'] = -10 
        print(' ')
            
class HarambeTrolley(AbstractTrolley):
    def __init__(self):
        AbstractTrolley.__init__(self)
        self.uppertrack = random.randint(3, 37)
        self.lowertrack = .3
        self.entropy = .02
        self.make_text()
        
    def make_text(self):
        self.lowertracktext = 'Harambe, a gorilla.'
        self.uppertracktext = 'no one. But if you pull the lever, then Harambe would never become a meme, and nobody will ever remember his life. \nWhat do you value more, Harambe or the idea of Harambe?'
    
    def gorilla_utils_txt(self):
        print("As a gorilla, Harambe is intrinsically worth %s utils" %(self.lowertrack))
        time.sleep(1)
        print("However, the joy his memes would have brought, as well as the impact on the animal rights movement, is well worth %s utils" % (self.uppertrack))
    
    def update_scores(self, move):
        time.sleep(1)
        diff = self.uppertrack - self.lowertrack
        if move:
            print("You have chosen to let the gorilla live, and for the meme to die.")
            time.sleep(2)
            self.gorilla_utils_txt()
            time.sleep(3)
            print("You have made the wrong decision.")
            time.sleep(1)
            print("Lose %s utils!" %(diff))
            self.pointchange['utils'] = -diff
        else:
            print("You chose to let Harambe die, so that the meme can live.")
            time.sleep(2)
            self.gorilla_utils_txt()
            time.sleep(3)
            print("You have made the correct decision.")
            time.sleep(1)
            print("Gain %s utils" %(diff))
            self.pointchange["utils"] = diff
        
        print("")
        time.sleep(.5)
        
        if move:
            print("You decided to save Harambe's life.")
            print("You have a hypothetical imperative to save lives, but not a categorical one.")
            print("Gain .1 Kant points")
            self.pointchange["kantpoints"] = .1 
        else:
            self.kant_default()

class BookTrolley(AbstractTrolley):
    def __init__(self):
        AbstractTrolley.__init__(self)
        self.make_books()
        self.entropy = .2
        self.bookutils = random.randint(3,10)
        
    def make_books(self):
        utilbooks = ["John Stuart Mill's 'Utilitarianism'", "An Introduction to the Principles of Morals and Legislation by Jeremy Bentham", "Animal Liberation by Peter Singer"]
        deonbooks = ["Groundwork for the Metaphysics of Morals by Kant","A Critique of Practical Reason by Kant", "A Theory of Justice by John Rawls"]
        utiltext = "the last surviving copy of " + random.choice(utilbooks) + ', a seminal text of utilitarianism.'
        deontext = "the last surviving copy of " + random.choice(deonbooks) + ', a well-regarded text of deontology.'
        self.utiltrack = random.randint(0,1) #0 is upper track, 1 is lower.
        if self.utiltrack == 0:
            self.uppertracktext = utiltext
            self.lowertracktext = deontext
        else:
            self.uppertracktext = deontext
            self.lowertracktext = utiltext
        
    def update_scores(self, move):
        if (move and self.utiltrack == 0) or (not move and self.utiltrack):
            print("You have allowed a great book of utilitarianism to be destroyed, for a mere deontological text!")
            time.sleep(2)
            print("Lose %s utils!" %(self.bookutils))
            self.pointchange['utils'] = -self.bookutils
        else:
            print("You have successfully identified the consequentially correct book to save.")
            print("You are a moral hero.")
            time.sleep(2)
            print("Gain %s utils!" %(self.bookutils))
            self.pointchange['utils'] = self.bookutils
        print("")
        time.sleep(2)
        if not move:
            self.kant_default()
        elif move and self.utiltrack == 0:
            print("You have successfully saved a deontological text.")
            print("However, spreading deontology is a hypothetical imperative, not a categorical one.")
            time.sleep(2.5)
            print("Gain 1 Kant point.")
            self.pointchange['kantpoints'] = 1 
        else:
            print("You have destroyed a great deontological text!")
            print("However, spreading deontology is a hypothetical imperative, not a categorical one.")
            time.sleep(2.5)
            print("Lose 1 Kant point.")
            self.pointchange['kantpoints'] = -1 

class DrowningChild(Dilemma):
    def __init__(self):
        Dilemma.__init__(self)
        self.decisionmsg = "Do you jump in to save the children? [Jump/Don't Jump] "
        self.clothes = random.randint(500,2000)
        self.children = random.randint(0,8)
        self.entropy = .5
        
    def that_childs_name(self):
        inventions = ['invent a perfect malaria vaccine', 'broker an international peace treaty', 'engineer an early-detection system for asteroids']
        childnames = ['Albert Einstein', 'Peter Singer', 'John Stuart Mill']
        invention = random.choice(inventions)
        child = random.choice(childnames)
        print('')
        print("One of the children you rescued went on to do great things.")
        print("He was so inspired by your sacrifice that he went on to %s, saving millions of lives." %(invention))
        time.sleep(2)
        print('')
        print("That child's name? %s." %(child))
        print('')
        print('Unfortunately, consequentialist ethics should not take into account moral luck, and you are not any more morally praiseworthy for somebody who turned out to be great, if you could not have anticipated this beforehand.')
        self.entropy = .2
        time.sleep(4)
        
    def print_dilemma(self):
        print('You are casually walking home from a long day at work, wearing an expensive suit and shoes that cost $ %s dollars.' %(self.clothes))
        time.sleep(2)
        print("As you come across a shallow pond, you hear splashing. Looking around, you see that %s children are drowning!" %(self.children))
        time.sleep(2)
        print("Nobody else is around. The pond is shallow so you're at no physical risk, but jumping in to save them will completely ruin your very expensive clothes.")
        print('')
        time.sleep(3)
        
    
    def print_decision(self, move):
        if move:
            print("You jump in to rescue the children, pulling them out one by one.")
            print("You rescue all of them!")
            time.sleep(2)
            print("You completely ruin your shoes in doing so, but you consider your sacrifice well worth it.")
        else:
            print(" 'It was a difficult job', you thought to yourself, 'but somebody had to do it.'")
            print("As you walk away from the screaming, you idly wonder to yourself who that somebody might be.")
        print(' ')
        time.sleep(2)
        
    def update_scores(self, move):
        if move and self.children >= 1:
            print("You rushed in and saved %s children's lives, at great personal sacrifice." %(self.children))
            if random.randint(1, 5) <= 1:
                self.that_childs_name()
            print("Gain %s utils!" %(self.children))
            self.pointchange['utils'] = self.children
        elif move and self.children == 0:
            print("While trying to save children from drowning is noble, it isn't when there aren't actually any children to save!")
            time.sleep(1)
            print("The money that it would take to replace your expensive clothes should have been spent on something else, like malarial bednets.")
            loss = round(self.clothes/4000.0, 3)
            print ('Lose %s utils!' % (loss))
            self.pointchange['utils'] -= loss
        if not move and self.children == 0:
            print("You made the pragmatic utilitarian decision.")
            print('Gain 0 utils.')
            self.pointchange['utils'] = 0 
        elif not move:
            print("You are a bystander, even though you could easily have saved the drowning children.")
            time.sleep(2)
            print("You are consequentially indistinguishable from a murderer.")
            print("Lose %s utils!" %(self.children))
            self.pointchange['utils'] = -self.children
        
        time.sleep(1)
        print('')
        
        if move and self.children > 0:
            print('Saving children is a noble cause, but it is superergoratory.')
            print("Gain 1 Kant point.")
            self.pointchange['kantpoints'] = 1 
        elif move:
            print("Prudence is nice, but it is not a categorical imperative.")
            print('Gain 0 Kant points')
            self.pointchange['kantpoints'] = 0 
        else:
            self.kant_default()
            
          
    
    def io(self):
        choice = input(self.decisionmsg)
        legalchoices = set(['j','y','t','s','f','n','d'])
        while len(choice) == 0 or choice[0].lower() not in legalchoices:
            print ("I didn't catch that...You HAVE to make a choice.")
            choice = input(self.decisionmsg)
        jump = False
        if choice[0].lower() in ['j','y','t','s']:
            jump = True
        return jump
        
g = Game()
g.play()