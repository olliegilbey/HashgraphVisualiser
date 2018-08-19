package hashgraphvisualizersdk;

import com.swirlds.platform.Address;
import com.swirlds.platform.AddressBook;
import com.swirlds.platform.FCDataInputStream;
import com.swirlds.platform.FCDataOutputStream;
import com.swirlds.platform.FastCopyable;
import com.swirlds.platform.Platform;
import com.swirlds.platform.SwirldState;
import java.io.IOException;
import java.time.Instant;

public class HashgraphState implements SwirldState {

	private AddressBook addressBook;
	
	@Override
	public synchronized void init(Platform platform, AddressBook addressBook) {
		this.addressBook= addressBook;
	}

	@Override
	public AddressBook getAddressBookCopy() {
		return addressBook.copy();
	}

	@Override
	public synchronized void copyFrom(SwirldState state) {
		addressBook = ((HashgraphState) state).addressBook;
	}

	@Override
	public synchronized void handleTransaction(long id, boolean isConsensus, Instant timestamp, byte[] trans, Address address) {
	}

	@Override
	public void noMoreTransactions() {
	}

	@Override
	public synchronized FastCopyable copy() {
		HashgraphState copy = new HashgraphState();
		copy.copyFrom(this);
		return copy;
	}

	@Override
	public void copyTo(FCDataOutputStream stream) throws IOException {
		addressBook.copyTo(stream);
	}

	@Override
	public void copyFrom(FCDataInputStream stream) throws IOException {
		addressBook.copyFrom(stream);
	}
	
}
