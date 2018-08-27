
import java.nio.charset.StandardCharsets;

import com.swirlds.platform.Event;
import com.swirlds.platform.Platform;
import com.swirlds.platform.SwirldMain;
import com.swirlds.platform.SwirldState;
import java.io.BufferedWriter;
import java.io.OutputStreamWriter;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.ArrayList;

/**
 * Creates a node which constantly sends out it's name with a counter. TODO implement occasional
 * dumps of the events for later processing
 */
public class HashgraphVisualizerSDKMain implements SwirldMain {

	/**
	 * the platform running this app
	 */
	public Platform platform;
	/**
	 * ID number for this member
	 */
	public long selfId;
	/**
	 * sleep this many milliseconds after each sync
	 */
	public final int sleepPeriod = 100;
	// Socket connection for dumping data
	private BufferedWriter dataStream;
	// last event sent by socket
	private long lastEvent = 0;

	@Override
	public void preEvent() {
	}

	@Override
	public void init(Platform platform, long id) {
		this.platform = platform;
		this.selfId = id;
		platform.setAbout("HashgraphSDK\n"); // set the browser's "about" box
		platform.setSleepAfterSync(sleepPeriod);
	}

	@Override
	public void run() {
		String myName = platform.getState().getAddressBookCopy()
				  .getAddress(selfId).getSelfName(); // name of event creator
		int count = 0; // event counter
		String lastReceived = "";

		System.out.println("Hello Swirld from " + myName);

		// Alice dumps events to the socket
		if (myName.equals("Alice")) {
			try {
				ServerSocket ss = new ServerSocket(54321);
				Socket conn = ss.accept();
				dataStream = new BufferedWriter(new OutputStreamWriter(conn.getOutputStream()));
			} catch (Exception e) {
			}
		}

		while (true) {

			// Create the transaction as a string of utf-8 characters consisting of
			// a node's name and the transaction counter
			byte[] transaction = (myName + count++).getBytes(StandardCharsets.UTF_8);
			// Send the transaction. The platform passes the transaction to our state
			// and to the local community. The community decides the order together
			platform.createTransaction(transaction);
			HashgraphState state = (HashgraphState) platform
					  .getState();
			String received = state.getReceived();

			if (!lastReceived.equals(received)) {
				lastReceived = received;
				System.out.println(myName + " received: " + received); // print all received transactions
			}

			if (myName.equals("Alice")) {
				System.out.println(myName + " is dumping events...");
				ArrayList<Event> lastEvents = new ArrayList<>(); // stores last events to calculate latest event
				for (Event event : platform.getAllEvents()) {
					if (event.getConsensusOrder() > lastEvent) {
						try {
							// write event information to socket for new events
							dataStream.append("{"
									  + "selfParentConsensusOrder:" + event.getSelfParent().getConsensusOrder() + ","
									  + "otherParentConsensusOrder:" + event.getOtherParent().getConsensusOrder() + ","
									  + "ownConsensusOrder:" + event.getConsensusOrder() + ","
									  + "timestamp:" + event.getConsensusTimestamp()
									  + "}\n");
						} catch (Exception e) {
						}
						lastEvents.add(event);
					}
				}
				try {
					dataStream.flush();
				} catch (Exception e) {
				}
				// calculate latest event
				for (Event event: lastEvents) {
					if (event.getConsensusOrder() < lastEvent) {
						lastEvent = event.getConsensusOrder();
					}
				}
			}

			try {
				Thread.sleep(sleepPeriod);
			} catch (Exception e) {
			}
		}
	}

	@Override
	public SwirldState newState() {
		return new HashgraphState();
	}
}
