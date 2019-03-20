/*
 *	Author: Arjan de Haan (Vepnar)
 */

import java.awt.*;
import java.awt.event.*;
import java.util.*;
import java.util.Timer;

import javax.swing.*;

public class ReactionSpeedTest extends JFrame implements MouseListener {
	
	private static final long serialVersionUID = 1L;
	private static ReactionSpeedTest instance;
	
	private enum gamestates {
		WAITING, FINISHED, CLICKNOW
	}
	
	private Timer timer = null;
	private Random rand = new Random();
	
	private long change = 0L;
	private gamestates gamestate = gamestates.FINISHED;
	private JLabel jl = new JLabel();	

	public static void main(String args[]) {
		instance = new ReactionSpeedTest();
	}
	
	public ReactionSpeedTest() {
		setSize(800,600);
		setResizable(false);
		setTitle("Reaction Speed Test");
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		addMouseListener(this);
		
		String fontFamily = jl.getFont().getFamily();
		Font newFont = new Font(fontFamily, 1, 30);
		jl.setFont(newFont);
		
		jl.setForeground(Color.WHITE);
		jl.setHorizontalAlignment(JLabel.CENTER);
		jl.setText("Click here to start");
		
		backgroundColor(Color.BLUE);
		
		add(jl);
		setVisible(true);	
	}
	
	private void backgroundColor(Color c) {
		getContentPane().setBackground(c);
	}

	private void stopTimer() {
		timer.cancel();
		timer.purge();
	}
	
	private void startTimer() {
		timer = new Timer();
		gamestate = gamestates.WAITING;
		int delay = rand.nextInt(3000);
		timer.schedule(new TimerTask() {
			
			@Override
			public void run() {
				instance.updateClickNow();
			}
			
		}, delay+1000);
		
		timer.schedule(new TimerTask() {
			@Override
			public void run() {
				instance.updateTooSlow();
			}
			
		}, delay+4000);
	}
	
	private void updateClickNow() {
		gamestate = gamestates.CLICKNOW;
		backgroundColor(Color.GREEN);
		jl.setText("Click now!");
		change = System.currentTimeMillis();
		
	}
	
	private void updateTooSlow() {
		stopTimer();
		gamestate = gamestates.FINISHED;
		jl.setText("You're too slow");
		backgroundColor(Color.RED);
		
	}
	private void updateTooSoon() {
		stopTimer();
		gamestate = gamestates.FINISHED;
		jl.setText("You clicked too early");
		backgroundColor(Color.RED);
	}
	
	private void updateClicked() {
		long speed = System.currentTimeMillis() - change;
		stopTimer();
		gamestate = gamestates.FINISHED;
		backgroundColor(Color.BLUE);
		jl.setText("Your reaction speed is:\n " + speed + "ms!");
		
	}
	
	private void updateWaiting() {
		startTimer();
		gamestate = gamestates.WAITING;
		jl.setText("Click when green");
		backgroundColor(Color.BLUE);
	}	
	
	@Override
	public void mousePressed(MouseEvent e) {
		switch(gamestate) {
		case CLICKNOW:
			updateClicked();
			break;
		case WAITING:
			updateTooSoon();
			break;
		default:
			updateWaiting();
			break;
		}
		
	}

	@Override
	public void mouseClicked(MouseEvent e) {}

	@Override
	public void mouseEntered(MouseEvent e) {}

	@Override
	public void mouseExited(MouseEvent e) {}

	@Override
	public void mouseReleased(MouseEvent e) {}
		
}
